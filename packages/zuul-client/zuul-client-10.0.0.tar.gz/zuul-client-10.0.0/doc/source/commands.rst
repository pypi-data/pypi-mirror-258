:title: Commands

Commands
========

Privileged commands
-------------------

Some commands require the user to be authenticated (and authorized). Zuul-client
supports two forms of authentication:

* **user/password** - Zuul-client will exchange the credentials for an access token
  on behalf of the user. This requires the identity provider to enable OpenID
  Connect's "password" grant type (also known as Direct Access Grant).
* **raw JWT** - The access token can be passed directly to zuul-client as the ``--auth-token``
  argument. Administrators can generate such a token for users as needed; an authenticated
  user on Zuul's Web UI can also fetch their currently valid token on the UI's user page.

Usage
-----
The general options that apply to all subcommands are:

.. program-output:: zuul-client --help

The following subcommands are supported:

Autohold
^^^^^^^^

.. note:: This command is only available with a valid authentication token.

.. program-output:: zuul-client autohold --help

Example::

  zuul-client autohold --tenant openstack --project example_project --job example_job --reason "reason text" --count 1

Autohold Delete
^^^^^^^^^^^^^^^

.. note:: This command is only available with a valid authentication token.

.. program-output:: zuul-client autohold-delete --help

Example::

  zuul-client autohold-delete --tenant openstack --id 0000000123

Autohold Info
^^^^^^^^^^^^^
.. program-output:: zuul-client autohold-info --help

Example::

  zuul-client autohold-info --tenant openstack --id 0000000123

Autohold List
^^^^^^^^^^^^^
.. program-output:: zuul-client autohold-list --help

Example::

  zuul-client autohold-list --tenant openstack

Builds
^^^^^^
.. program-output:: zuul-client builds --help

Examples::

  zuul-client --use-conf sfio builds --tenant mytenant --result NODE_FAILURE
  zuul-client --use-conf opendev builds --tenant zuul --project zuul/zuul-client --limit 10

Build-info
^^^^^^^^^^
.. program-output:: zuul-client build-info --help

Examples::

  zuul-client build-info --tenant mytenant --uuid aaaaa
  zuul-client build-info --tenant mytenant --uuid aaaaa --show-job-output

Dequeue
^^^^^^^

.. note:: This command is only available with a valid authentication token.

.. program-output:: zuul-client dequeue --help

Examples::

    zuul-client dequeue --tenant openstack --pipeline check --project example_project --change 5,1
    zuul-client dequeue --tenant openstack --pipeline periodic --project example_project --ref refs/heads/master

Encrypt
^^^^^^^
.. program-output:: zuul-client encrypt --help

Examples::

    zuul-client encrypt --tenant openstack --project config --infile .pypirc --outfile encrypted.yaml --secret-name pypi_creds --field-name pypirc
    cat .pypirc | zuul-client encrypt --tenant openstack --project config

Enqueue
^^^^^^^

.. note:: This command is only available with a valid authentication token.

.. program-output:: zuul-client enqueue --help

Example::

  zuul-client enqueue --tenant openstack --trigger gerrit --pipeline check --project example_project --change 12345,1

Note that the format of change id is <number>,<patchset>.

Enqueue-ref
^^^^^^^^^^^

.. note:: This command is only available with a valid authentication token.

.. program-output:: zuul-client enqueue-ref --help

This command is provided to manually simulate a trigger from an
external source.  It can be useful for testing or replaying a trigger
that is difficult or impossible to recreate at the source.  The
arguments to ``enqueue-ref`` will vary depending on the source and
type of trigger.  Some familiarity with the arguments emitted by
``gerrit`` `update hooks
<https://gerrit-review.googlesource.com/admin/projects/plugins/hooks>`__
such as ``patchset-created`` and ``ref-updated`` is recommended.  Some
examples of common operations are provided below.

Manual enqueue examples
***********************

It is common to have a ``release`` pipeline that listens for new tags
coming from ``gerrit`` and performs a range of code packaging jobs.
If there is an unexpected issue in the release jobs, the same tag can
not be recreated in ``gerrit`` and the user must either tag a new
release or request a manual re-triggering of the jobs.  To re-trigger
the jobs, pass the failed tag as the ``ref`` argument and set
``newrev`` to the change associated with the tag in the project
repository (i.e. what you see from ``git show X.Y.Z``)::

  zuul-client enqueue-ref --tenant openstack --trigger gerrit --pipeline release --project openstack/example_project --ref refs/tags/X.Y.Z --newrev abc123...

The command can also be used asynchronosly trigger a job in a
``periodic`` pipeline that would usually be run at a specific time by
the ``timer`` driver.  For example, the following command would
trigger the ``periodic`` jobs against the current ``master`` branch
top-of-tree for a project::

  zuul-client enqueue-ref --tenant openstack --trigger timer --pipeline periodic --project openstack/example_project --ref refs/heads/master

Another common pipeline is a ``post`` queue listening for ``gerrit``
merge results.  Triggering here is slightly more complicated as you
wish to recreate the full ``ref-updated`` event from ``gerrit``.  For
a new commit on ``master``, the gerrit ``ref-updated`` trigger
expresses "reset ``refs/heads/master`` for the project from ``oldrev``
to ``newrev``" (``newrev`` being the committed change).  Thus to
replay the event, you could ``git log`` in the project and take the
current ``HEAD`` and the prior change, then enqueue the event::

  NEW_REF=$(git rev-parse HEAD)
  OLD_REF=$(git rev-parse HEAD~1)

  zuul-client enqueue-ref --tenant openstack --trigger gerrit --pipeline post --project openstack/example_project --ref refs/heads/master --newrev $NEW_REF --oldrev $OLD_REF

Note that zero values for ``oldrev`` and ``newrev`` can indicate
branch creation and deletion; the source code of Zuul is the best reference
for these more advanced operations.

Freeze-job
^^^^^^^^^^

Display information about a job as it would be run in a particular
project's pipeline.  This causes Zuul to combine all of the matching
jobs and variants that would be used to form the final version of a
job that would be executed for a change or ref as enqueued into the
specified pipeline.  This includes job attributes, playbook paths,
nodesets, variables, etc.  Secret names may be included but the values
are redacted.

The default text output shows an abbreviated summary of only the most
pertinent information.  The JSON output reports all available
information.

.. program-output:: zuul-client freeze-job --help

Example::

  zuul-client freeze-job --tenant mytenant --pipeline check --project org/project --branch master --job tox

Job-graph
^^^^^^^^^

Display the set of jobs that would be triggered in a project's
pipeline.  This will show the complete set of jobs that Zuul will
consider running if an item for the given project and branch were
enqueued into the specified pipeline.  Information about job
dependencies (soft and hard) is also included.  The actual set of jobs
run for a given change or ref may be less than what is output by this
command if some jobs have non-matching file matchers.

This command supports the ``dot`` output format.  When used, the
output may be supplied to graphviz in order to render a graphical view
of the job graph.

.. program-output:: zuul-client job-graph --help

Example::

  zuul-client job-graph --tenant mytenant --pipeline check --project org/project --branch master
  zuul-client --format dot job-graph --tenant mytenant --pipeline check --project org/project --branch master | xdot

Promote
^^^^^^^

.. note:: This command is only available with a valid authentication token.

.. program-output:: zuul-client promote --help

This command will push the listed changes at the top of the chosen pipeline.

Example::

  zuul-client promote --tenant openstack --pipeline check --changes 12345,1 13336,3

Note that the format of changes id is <number>,<patchset>.

The promote action is used to reorder the change queue in a pipeline, by putting
the provided changes at the top of the queue; therefore this action makes the most
sense when performed against a dependent pipeline.

The most common use case for the promote action is the need to merge an urgent fix
when the gate pipeline has already several patches queued ahead. This is especially
needed if there is concern that one or more changes ahead in the queue may fail,
thus increasing the time to land for the fix; or concern that the fix may not
pass validation if applied on top of the current patch queue in the gate.

If the queue of a dependent pipeline is targeted by the promote, all the ongoing
jobs in that queue will be canceled and restarted on top of the promoted changes.
