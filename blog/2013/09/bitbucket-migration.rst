At work, we are currently using Launchpad for project hosting of our
proprietary codebase. Launchpad charges $250/year/project for hosting of
proprietary projects which is a little steep, and Launchpad/bzr has been
falling behind the alternatives in terms of tooling / development / support, so
when our Launchpad subscription came up for renewal at the beginning of the
month, this caused our somewhat vague plans to switch to something else to
crystalize.

I initially assumed that Github/git would be the obvious way to go, but after
looking into BitBucket/hg, I was pleasantly surprised to discover that things
like hosted CI were available there too. Nobody on our team is much of a git
enthusiast to begin with, so using hg seemed like a far more attractive option.
This meant figuring out how to do two things: 1) migrate all of our existing
bugs, and 2) migrate our existing bzr branches to hg. The former proved to be
relatively straightforward: Jonathan_ wrote a script that used launchpadlib to
access the Launchpad API, retrieve the bug data + metadata, and write it out in
the BitBucket import format (more on this in another post, or on Jonathan's
blog, depending on if I can convince him to write it up or not).

.. _Jonathan: http://jonathan.jsphere.com/

The bzr to hg conversion turned out to be a little more complex. A simple "hg
convert" of our trunk branch worked surprisingly well; the trunk history
converted correctly (at least as far as I could tell), but more (pleasantly)
surprisingly, the branches which were merged into trunk were also reconstructed
by the conversion, along with the merges. The conversion relies on the bzr
branch nick; this works somewhat like hg branches (it's associated with a
commit at the time that you commit), but as bzr does not place as much
importance on this label as hg, it is more likely to be wrong by accident (by
default the branch nick is just taken from the last component of the path to
the branch you are committing in, I believe, and in our case I suspect nobody
has ever set the branch nick manually). Among other things, this resulted in 4
different branch names for "trunk", as well as some other oddities like
misspelled feature branch names.

(As an aside, I'd like to mention that ``hg log`` has far more utility than
``bzr log``, mostly due to the "revsets" feature. Almost all of the inspection
I did while debugging the conversion was done on the converted repo using hg,
not on the original bzr repo, simply because it was far easier to get the
information that way.)

A "branchmap" file solved the problem with differing branches; mapping the
different names for "trunk" to "default" made the revision history graph look a
lot more reasonable than when I originally did the conversion. I also switched
to using ``--datesort`` for the conversion at this point; the documentation
warns that this may produce a much larger repository than ``--branchsort (the
default)``, but in my case, the size difference was trivial. I suspect this may
only apply in scenarios with back-and-forth merges between long-lived branches,
rather than the short-lived topic branches that form the majority of our
workflow. I also created an "authormap" file at this point to reconcile
differing author identities over the history of our repository. The bzr author
identity is a full name/email (eg. "Tristan Seligmann
<mithrandi@mithrandi.net>", but again, there were various historical oddities
here; BitBucket also has the ability to map author identities to BitBucket
users, but I decided normalizing during the conversion was a good idea anyway.

The biggest problem I had to deal with (although this was actually one of the
first problems I noticed) was that all of these merged branches were still
open. Mercurial has the concept of "open" and "closed" branches, with closed
branches being hidden by default in most places. A "closed" branch is simply
one whose head revision is marked as closing the branch; which of course, none
of my branches had, due to being converted from bzr which does not have an
equivalent concept. Committing a closing revision to each branch was simple
enough to script, but that only lead to more difficulties: 1) a gigantic pile
of noise revisions in the history, and 2) a bunch of dangling heads as the new
"close" revision was not part of the merge to trunk. Scripting a merge of all
of the dangling heads would have produced even more noise, so I looked for a
different solution.

Eventually I ran across a patch_ on the Mercurial mailing list; unfortunately
the thread in which it was posted never went anywhere, but the patch still
worked. What this patch allowed me to do was after the initial conversion, run
another hg-to-hg conversion in which I marked the last branch revision before
the merge to trunk as closing the branch. The full conversion process now
looked something like this:

.. _patch: http://www.selenic.com/pipermail/mercurial-devel/2013-January/047450.html

.. code:: bash

   hg convert --datesort --branchmap branchmap --authormap authormap Fusion Fusion-hg-unspliced
   cd Fusion-hg-unspliced
   hg log --template "{node} close\n" -r "head() and not branch(default)" > ../splicemap
   cd ..
   PYTHONPATH=$HOME/hg-patched python $HOME/hg-patched/hg convert --splicemap splicemap Fusion-hg-unspliced Fusion-hg

This was good enough for a trunk conversion, but what about open branches that
aren't yet merged into trunk? We could have held off until we were able to
merge all of these branches, but that seemed like a lot of work (although we
did merge as many outstanding branches as possible). Fortunately hg convert can
operate in an incremental way; during the conversion, the mapping from source
revs to destination revs is stored in dest/.hg/shamap; the only wrinkle was my
two stage-conversion process. What I needed was a way to map the original bzr
revisions to the hg revisions in the *second* repository. In order to
accomplish this, I wrote a small Python script to merge the two mappings:

.. gist:: a71bffcdc4e42496e39a6a659aa1fe7f


With the help of this script, I could now convert other branches:

.. code:: bash

   # Only take the bzr revisions
   grep '@' Fusion-hg-unspliced/.hg/shamap > shamap
   python mergemaps.py shamap Fusion-hg/.hg/shamap > shamap-spliced
   mv shamap-spliced Fusion-hg/.hg/shamap

   # Now let's convert a branch
   hg convert --branchmap branchmap --authormap authormap Fusion-some-branch Fusion-hg

In summary, the process, while hardly trivial, worked out a lot better than I
had initially expected.

EDIT: I forgot to mention in the original draft: We first started thinking
about moving away from Launchpad at the beginning of September, and completed
the migration in the last week, so the entire process took us less than a month
of part-time discussion / work.
