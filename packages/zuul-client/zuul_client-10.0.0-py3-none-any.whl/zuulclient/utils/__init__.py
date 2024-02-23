# Copyright 2020 Red Hat, inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import base64
import math
import os
import re
import subprocess

import requests


def get_default(config, section, option, default=None, expand_user=False):
    if config.has_option(section, option):
        # Need to be ensured that we get suitable
        # type from config file by default value
        if isinstance(default, bool):
            value = config.getboolean(section, option)
        elif isinstance(default, int):
            value = config.getint(section, option)
        else:
            value = config.get(section, option)
    else:
        value = default
    if expand_user and value:
        return os.path.expanduser(value)
    return value


def encrypt_with_openssl(pubkey_path, plaintext, logger=None):
    cmd = ['openssl', 'version']
    if logger:
        logger.debug('Invoking "%s"' % ' '.join(cmd))
    try:
        openssl_version = subprocess.check_output(
            cmd).split()[1]
    except FileNotFoundError:
        raise Exception('"openssl" is not installed on the system')

    cmd = ['openssl', 'rsa', '-text', '-pubin', '-in', pubkey_path]
    if logger:
        logger.debug('Invoking "%s"' % ' '.join(cmd))
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    if p.returncode != 0:
        raise Exception('openssl failure (Return code %s)' % p.returncode)

    output = stdout.decode('utf-8')
    if openssl_version.startswith(b'0.'):
        key_length_re = r'^Modulus \((?P<key_length>\d+) bit\):$'
    else:
        key_length_re = r'^(|RSA )Public-Key: \((?P<key_length>\d+) bit\)$'
    m = re.match(key_length_re, output, re.MULTILINE)
    nbits = int(m.group('key_length'))
    nbytes = int(nbits / 8)
    max_bytes = nbytes - 42  # PKCS1-OAEP overhead
    chunks = int(math.ceil(float(len(plaintext)) / max_bytes))

    ciphertext_chunks = []

    if logger:
        logger.info(
            'Public key length: {} bits ({} bytes)'.format(nbits, nbytes))
        logger.info(
            'Max plaintext length per chunk: {} bytes'.format(max_bytes))
        logger.info(
            'Input plaintext length: {} bytes'.format(len(plaintext)))
        logger.info('Number of chunks: {}'.format(chunks))

    cmd = ['openssl', 'rsautl', '-encrypt',
           '-oaep', '-pubin', '-inkey',
           pubkey_path]
    if logger:
        logger.debug('Invoking "%s" with each data chunk:' % ' '.join(cmd))
    for count in range(chunks):
        chunk = plaintext[int(count * max_bytes):
                          int((count + 1) * max_bytes)]
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        if logger:
            logger.debug('\tchunk %s' % (count + 1))
        (stdout, stderr) = p.communicate(str.encode(chunk))
        if p.returncode != 0:
            raise Exception('openssl failure (Return code %s)' % p.returncode)
        ciphertext_chunks.append(base64.b64encode(stdout).decode('utf-8'))
    return ciphertext_chunks


def get_oidc_config(authority, verify=True):
    _authority = authority
    if not _authority.endswith('/'):
        _authority += ('/')
    oidc_config = requests.get(
        _authority + '.well-known/openid-configuration',
        verify=verify
    )
    oidc_config.raise_for_status()
    return oidc_config.json()


def is_direct_grant_allowed(oidc_config):
    return 'password' in oidc_config.get('grant_types_supported', [])


def get_token(username, password, client_id, oidc_config,
              scope=None, verify=True):
    token_endpoint = oidc_config.get('token_endpoint')
    _data = {
        'client_id': client_id,
        'username': username,
        'password': password,
        'grant_type': 'password',
    }
    if scope:
        _data['scope'] = scope
    response = requests.post(
        token_endpoint,
        verify=verify,
        data=_data
    )
    response.raise_for_status()
    token = response.json()['access_token']
    return token
