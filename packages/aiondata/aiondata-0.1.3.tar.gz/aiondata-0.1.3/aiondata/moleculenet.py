import os
from pathlib import Path
import polars as pl

from .datasets import CsvDataset


class Tox21(CsvDataset):
    """Tox21 is a dataset consisting of qualitative toxicity measurements for 12,000 compounds on 12 different targets."""

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv.gz"


class ESOL(CsvDataset):
    """
    ESOL is a dataset consisting of water solubility data for 1,128 compounds. The dataset is widely used for developing models that predict solubility directly from chemical structures.
    """

    SOURCE = (
        "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv"
    )


class FreeSolv(CsvDataset):
    """
    FreeSolv provides experimental and calculated hydration free energy of small molecules in water. It includes 642 molecules and is used for benchmarking hydration free energy predictions.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/SAMPL.csv"


class Lipophilicity(CsvDataset):
    """
    Lipophilicity contains experimental measurements of octanol/water distribution coefficient (logD at pH 7.4) for 4,200 compounds. It is useful for modeling compound partitioning between lipids and water.
    """

    SOURCE = (
        "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Lipophilicity.csv"
    )


class QM7(CsvDataset):
    """
    QM7 is a dataset of 7,165 molecules, which provides quantum mechanical properties that are computed using density functional theory (DFT). It's primarily used for regression tasks on molecular properties.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/qm7.csv"


class QM8(CsvDataset):
    """
    QM8 includes electronic spectra and excited state energy of small molecules computed using time-dependent DFT (TD-DFT). It consists of over 20,000 molecules and is used for regression of electronic properties.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/qm8.csv"


class QM9(CsvDataset):
    """
    QM9 dataset contains geometric, energetic, electronic, and thermodynamic properties of roughly 134,000 molecules with up to 9 heavy atoms, computed using DFT.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/qm9.csv"


class MUV(CsvDataset):
    """
    MUV (Maximum Unbiased Validation) datasets consist of 17 assays designed for validation of virtual screening techniques. It includes about 93,000 compounds across various assays.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/muv.csv.gz"


class HIV(CsvDataset):
    """
    HIV dataset contains data on the ability of compounds to inhibit HIV replication. It is used for binary classification tasks, with over 40,000 compounds.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/HIV.csv"


class BACE(CsvDataset):
    """
    BACE dataset includes quantitative binding results for a set of inhibitors of human beta-secretase 1 (BACE-1). It's used for both classification and regression tasks on over 1,500 compounds.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/bace.csv"


class BBBP(CsvDataset):
    """
    BBBP (Blood-Brain Barrier Penetration) dataset. It contains compounds with features regarding permeability properties across the Blood-Brain Barrier, used for binary classification tasks.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv"


class SIDER(CsvDataset):
    """
    SIDER contains information on marketed medicines and their recorded adverse drug reactions (ADR), used for multi-task classification of side effects.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/sider.csv.gz"


class ClinTox(CsvDataset):
    """
    ClinTox compares drugs approved by the FDA and those that have failed clinical trials for toxicity reasons. It's used for binary classification and toxicity prediction.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/clintox.csv.gz"
