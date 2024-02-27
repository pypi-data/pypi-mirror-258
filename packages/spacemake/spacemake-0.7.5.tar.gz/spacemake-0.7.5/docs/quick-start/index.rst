.. include:: ../links.rst

.. _Quick start guide main:

Quick start guide
=================

The examples here are minimal code pieces on how to quickly get started with spacemake.
It is assumed that spacemake has been instaled following the instructions :ref:`here <installation>`.

.. _Quick start guide initialize spacemake:

Initialize spacemake
--------------------

.. include:: ../shared/spacemake_init.rst


.. _Quick start guide shared sample-variables:

Shared sample-variables
-----------------------

.. include:: ../shared/shared_sample_variables.rst

As spacemake comes with no ``default`` value for ``species``, before anything can be done,
a new species has to be added::

   spacemake config add_species \
      --name \         # name of the species
      --reference \    # short-hand name of the sequence (default='genome')
      --sequence \     # path to .fa file
      --annotation \   # path to .gtf file
      --STAR_index_dir # (optional) path to an existing STAR index directory
      
More info :ref:`here <configure-species>`.

.. warning::

    If the ``--STAR_index_dir`` flag is provided spacemake will check if the STAR 
    index provided has the same version of STAR as the command-line STAR. If this is
    not the case, an error will be raised.

Visium quick start
------------------

Step 1: add a Visium sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After :ref:`spacemake has been initialized <initialization>`, a `Visium`_ sample can be added.

To add a `Visium`_ sample, type in terminal:

.. code-block:: console

   spacemake projects add_sample \
      --project_id <project_id> \
      --sample_id <sample_id> \
      --R1 <path_to_R1.fastq.gz> \ # single R1 or several R1 files
      --R2 <path_to_R2.fastq.gz> \ # single R2 or several R2 files
      --species <species> \
      --puck visium \
      --run_mode visium \
      --barcode_flavor visium

Above we add a new visium project with ``puck, run_mode, barcode_flavor`` all set to ``visium``.

This is possible as spacemake comes with pre-defined variables, all suited for visium. The visium ``run_mode`` will process the 
sample in the same way as `spaceranger <https://support.10xgenomics.com/spatial-gene-expression/software/pipelines/latest/what-is-space-ranger>`_ would: intronic reads will not be counted, multi-mappers (where the multi-mapping read maps only to one CDS or UTR region) will be counted,
3' polyA stretches will not be trimmed from Read2.

.. note::

   With the ``--R1`` and ``--R2`` it is possible to provide a single ``.fastq.gz`` file (one per mate) or several files per mate.
   For example, if the result of a demultiplexing run is as follows:
   
   ``sample_1a_R1.fastq.gz``, ``sample_1b_R1.fastq.gz``, ``sample_1a_R2.fastq.gz``, ``sample_1b_R2.fastq.gz``, meaning that
   R1 and R2 are both split into two, one can simply call spacemake with the following command::
      
      spacemake projects add_sample \
         ...
         --R1 sample_1a_R1.fastq.gz sample_1b_R1.fastq.gz \
         --R2 sample_1a_R2.fastq.gz sample_1b_R2.fastq.gz \

   The important thing is to always keep the order consistent between the two mates.

To see the values of these predefined variables checkout the :ref:`configuration <Configuration>` docs.

**To add several visium samples at once, follow** :ref:`the tutorial here <add-several-samples>`

.. _running spacemake Visium:

Step 2: running spacemake
^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: run_spacemake.rst 

Slide-seq quick start
---------------------

Step 1: add a Slide-seq sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After :ref:`spacemake has been initialized <initialization>`, a `Slide-seq`_ sample can be added.

To add a `Slide-seq`_ sample, type in terminal:

.. code-block:: console

   spacemake projects add_sample \
      --project_id <project_id> \
      --sample_id <sample_id> \
      --R1 <path_to_R1.fastq.gz> \
      --R2 <path_to_R2.fastq.gz> \
      --species <species> \
      --puck slide_seq \
      --run_mode slide_seq \
      --barcode_flavor slide_seq_14bc \
      --puck_barcode_file <path_to_puck_barcode_file>

Above we add a new `Slide-seq`_ project with the ``puck, run_mode`` will be set to ``slide_seq``
which are pre-defined settings for `Slide-seq`_ samples.

.. note::
   For spatial samples other than visium - such as `Slide-seq`_ - we need to provide a
   ``puck_barcode_file`` (since each puck has different barcodes, unlike for visium samples).
   This file should be a comma or tab separated, containing column names as first row. Acceptable column names are:

   - ``cell_bc``, ``barcodes``  or ``barcode`` for cell-barcode
   - ``xcoord`` or ``x_pos`` for x-positions
   - ``ycoord`` or ``y_pos`` for y-positions

In this example ``barcode_flavor`` will be set to ``slide_seq_14bc``,
a pre-defined ``barcode_flavor`` in spacemake, where the ``cell_barcode`` comes from the first 14nt of Read1, and the ``UMI`` comes from nt 13-22 (remaining 9 nt). 
The other pre-defined ``barcode_flavor`` for `Slide-seq`_ is ``slide_seq_15bc``: here ``cell_barcode`` again comes from the first 14nt of Read1, but the ``UMI`` comes from nt 14-22 (remaining 8) of Read1.

To see the values of these predefined variables checkout the :ref:`configuration <Configuration>` docs.

**To add several slide_seq projects at once, follow** :ref:`the tutorial here <add-several-samples>`

.. _running spacemake Slide-seq:

Step 2: running spacemake
^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: run_spacemake.rst 

Seq-scope quick start
---------------------

Step 1: add a Seq-scope sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After :ref:`spacemake has been initialized <initialization>`, a `Seq-scope`_ sample can be added.

Adding a `Seq-scope`_ sample 
is similar to Slide-seq:

.. code-block:: console

   spacemake projects add_sample \
      --project_id <project_id> \
      --sample_id <sample_id> \
      --R1 <path_to_R1.fastq.gz> \ # single R1 or several R1 files
      --R2 <path_to_R2.fastq.gz> \ # single R2 or several R2 files
      --species <species> \
      --puck seq_scope \
      --run_mode seq_scope \
      --barcode_flavor seq_scope \
      --puck_barcode_file <path_to_puck_barcode_file>

Here we used the pre-defined variables for ``puck``, ``barcode_flavor`` and ``run_mode`` all set to ``seq_scope``.

The ``seq_scope`` ``puck`` has 1000 micron width and bead size set to 1 micron.

The ``seq_scope`` ``barcode_flavor`` describes how the ``cell_barcode`` and he ``UMI`` should be extracted. 
As described in the `Seq-scope`_ paper.
``cell_barcode`` comes from nt 1-20 of Read1, and ``UMI`` comes from 1-9nt of Read2.

The ``seq_scope`` ``run_mode`` has its settings as follows:

.. code-block:: yaml

    seq_scope:
        clean_dge: false
        count_intronic_reads: false
        count_mm_reads: false
        detect_tissue: false
        mesh_data: true
        mesh_spot_diameter_um: 10
        mesh_type: hexagon
        n_beads: 1000
        umi_cutoff:
        - 100
        - 300

The most important thing to notice here that by default, we create a hexagonal mesh with
the ``seq_scope`` ``run_mode``. This means that downstream rather than with working with
the 1 micron beads, spaceame will create a mesh of adjascent, equal hexagons with 10 micron
sides.

.. _running spacemake Seq-scope:

Step 2: running spacemake
^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: run_spacemake.rst 

scRNA-seq quick start
---------------------

Step 1: add a single-cell RNA-seq sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

spacemake was written as a spatial-transcriptomics pipeline, however it will also work for
single-cell experiments, where there is no spatial information available. 

To add a scRNA-seq sample, simply type::

   spacemake projects add_sample \
      --project_id <project_id> \
      --sample_id <sample_id> \
      --R1 <path_to_R1.fastq.gz> \ # single R1 or several R1 files
      --R2 <path_to_R2.fastq.gz> \ # single R2 or several R2 files
      --species <species> \
      --run_mode scRNA_seq \
      --barcode_flavor default # use other flavors for 10X Chromium

As seen above, we define fewer variables as before: only ``species`` and ``run_mode`` are needed.

.. warning:: 

    As it can be seen, we set the ``barcode_flavor`` to ``default``, which will use the `Drop-seq`_ 
    scRNA-seq barcoding strategy (``cell_barcode`` is 1-12nt of Read1, ``UMI`` is 13-20 nt of Read1).

    For 10X samples either the ``sc_10x_v2`` (10X Chromium Single Cell 3' V2)
    or ``visium`` (10X Chromium Single Cell 3' V3, same as visium) should be be used as
    ``barcode_flavor``. Both are pre-defined in spacemake.
    
    If another barcoding strategy is used, a custom ``barcode_flavor`` has to be defined.
    :ref:`Here is a complete guide on how to add a custom barcode_flavor <add a new barcode\\_flavor>`.

.. note:: 

    By setting ``run_mode`` to ``scRNA_seq`` we used the pre-defined ``run_mode`` settings tailored for single-cell experiments: expected number of cells (or beads) will be 10k, introns will be counted, UMI cutoff will be at 500, multi-mappers will not be counted and polyA and adapter sequences will be trimmed from Read2. 

    Of course, running single-cell samples with other ``run_mode`` settings is also possible.

    :ref:`Here it can be learned how to add a custom run_mode <add a new run\\_mode>`, tailored to the experimental needs.

To see the values of these predefined variables checkout the :ref:`configuration <Configuration>` docs.

**To add several single-cell projects at once, follow** :ref:`the tutorial here <add-several-samples>`

.. _running spacemake scRNA-seq:

Step 2: running spacemake
^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: run_spacemake.rst 

