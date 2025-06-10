# crisprHAL — Adenine methylated PAM sequences inhibit SaCas9 activity
Note: this is a static paper-specific repository, and as such, may not contain up-to-date models. For the crisprHAL prediction tool, please visit the first link below or visit the website at the second link below.

## Links to the crisprHAL repositories, papers, and web tool:
* [Up-to-date crisprHAL prediction tool for use](https://github.com/tbrowne5/crisprHAL)
* [Online crisprHAL prediction tool](https://crisprhal.streamlit.app/)
* [crisprHAL 2.0 paper repository](https://github.com/tbrowne5/Better-data-for-better-predictions-data-curation-improves-deep-learning-for-sgRNA-Cas9-prediction/)
* crisprHAL 2.0 pre-print (Available soon)
* [crisprHAL SaCas9 paper repository](https://github.com/tbrowne5/Adenine-methylated-PAM-sequences-inhibit-SaCas9-activity) — **YOU ARE HERE**
* crisprHAL SaCas9 pre-print (Available soon)
* [crisprHAL SpCas9 paper repository](https://github.com/tbrowne5/A-generalizable-Cas9-sgRNA-prediction-model-using-machine-transfer-learning)
* [crisprHAL SpCas9 publication](https://doi.org/10.1038/s41467-023-41143-7)

## ABSTRACT

Cas9 nucleases can be used with single guide RNAs (sgRNAs) as antimicrobials and genome engineering tools in bacteria, yet applications are hindered by an incomplete understanding of Cas9-target interactions. Here, we generate large-scale SaCas9/sgRNA *in vivo* bacterial activity datasets and train a machine learning model (crisprHAL) to predict SaCas9 activity. The highest predictive performance was found when downstream sequence flanking the canonical NNGRRN PAM motif at positions \[+1] and \[+2] was included in model training, correlating with high *in vivo* activity on sites that included T-rich di-nucleotides in the \[+1] and \[+2] flanking positions. Strikingly, model predictions and experimentally determined activity in pooled sgRNA experiments in *Escherichia coli* and *Citrobacter rodentium* showed significantly reduced SaCas9 activity at sites with 5'-NNGGAT\[C]-3' PAM sequences. Adenine methylation (\*A) at 5'-NNGG\*AT\[C]-3' PAMs reduced SaCas9 activity ~10 fold, whereas cytosine methylation (5'-NNGGAT\[*C]-3' had no impact on activity. Our results show that a general purpose machine learning architecture can provide biologically relevant insights into SaCas9-PAM interactions that can better inform activity predictions. Avoidance of adenine methylated PAM sites by SaCas9 may be a mechanism of self versus non-self discrimination or reflect an evolutionary adaptation to counter methylation as an anti-restriction strategy by phage or plasmids.

## FILES AND DIRECTORIES:
* data/ contains raw data, model training data, and hold-out test set
* models/ contains the model save
* crisprHAL.py contains the main Python script for model running
* model.py contains the code for running the models
* processing.py contains the code for input data processing

## QUICK START

If you wish to run the model on your own nucleotide sequence follow parts 0 to 3. 

If you wish to validate the model predictions or training, follow parts 4 to 5.

If you wish to simply obtain predictions, you can do so easily through the [crisprHAL website](https://crisprHAL.streamlit.app).

**Please be advised:** This is a paper-specific repository, for practical use with the most up-to-date models, please visit the [crisprHAL](https://github.com/tbrowne5/crisprHAL) repository.

## SECTIONS OF THIS GUIDE:

Setting up and running the model to predict sgRNA/Cas9 activities:
* 0: Model requirements ```Time: 1-10 minutes```
* 1: Running the model test ```Runtime: 10 seconds```
* 2: Understanding available model options
* 3: Predicting with the model ```Runtime: 1-10 seconds```

Additional information and methods: 
* 4: Preparing your own model input files & comparing predictions
* 5: Validating the trained models ```Variable runtime```
* 6: Data availability and processing
* 7: Citations
* 8: How to cite this model

## 0: Requirements

These are in a file called requirements.txt and should be in the working directory.
```
python
tensorflow
```

These can be instantiated within a conda environment: ```Time: 1-10 minutes```

```
conda create --name HAL
conda activate HAL
conda install --file requirements.txt
```

This installation has been tested in Ubuntu 20.04.4 and Mac OSX 10.14.5, but has not been tested on Windows.


## 1: Run the model test
```
python crisprHAL.py
```
Test our primary SpCas9/TevSpCas9 prediction model: crisprHAL Tev

Success here is that the model runs without error, showing that it is installed correctly. ```Runtime: ~10 seconds```


## 2: Understand options

```
python crisprHAL.py [options]
```
```
--input, -i   [Input file path]
```
Input: crisprHAL accepts three types of input files: FASTA (.fasta and .fa), CSV (.csv), and TSV (.tsv). If no input is specified, the model will default to testing on its respective hold-out set.

```
--output, -o  [Output file path]
```
Output: specify the output path and file name of choice. If no output is specified, output file will have the input file name with the prefix: "_predictions.txt"
```
--circular
```
Circular (default=FALSE): specific to FASTA inputs; specifies that the input sequence should be treated as circular DNA rather than linear.
```
--compare, -c
```
Compare (default=FALSE): specific to CSV/TSV inputs; specifies that the input file contains a second column with scores for comparison. Outputs Spearman and Pearson correlation coefficients between predictions and provided scores, and writes both the predictions and scores to the output file.
```
--train, -t
```
Train (default=FALSE): train the model using training dataset: ```data/TevSaCas9_training_data.csv```
```
--epochs, -e  [Integer epoch value]
```
Epochs: specify the number of training epochs to be run when training the model. By default each model uses its respective 5CV-identified epochs. Without the ```--train/-t``` flag, ```--epochs/-e``` will do nothing.
```
--help, -h
```
Help: prints available options.


## 3: Predict with the model

To run a test of the model's predictions, please run the command:
```
python crisprHAL.py -m TevSpCas9 -i sample.fa
```
This will: 1) Identify all sgRNA targets in the sample.fa file, 2) Predict Cas9 activity for each target, and 3) Write the targets and predicted activities to a file called sample_predictions.txt

The full list of options for FASTA input-based model predictions are:
```
python crisprHAL.py --model [TevSpCas9/eSpCas9/WT-SpCas9] --input [input file path] --output [optional output file path] --circular
```


## 4: Preparing your own input CSV Files

Input CSV file for prediction only, no "Compare" option:
```
ATGCATATCCCTCTTATTGCCGGTCGCG
GTCTTTATCAGCTAACCAGTCGGTATCC
CGATGGTCAATATCAGCCGTTGGCGCAG
TTTGCCTCATCAACACCTGAAGGCCTCA
CCGCTTTTCCTGCCTGACCTTGGGTGAA
CATAATAGTATTTCCGATAAGGGTCCCC
CGTAGCCGACAATACGGAAACGGTGAGT
CCGAGACGTTGATGCCAATATGGAAATT
CAGGAAACGGCTAACAGAACCGGACCAA
GTGGCAATCGTCGTTTTAACCGGCAAAC
```

Input CSV file for prediction and comparison of the predictions to scores in column 2:
```
CTCGATTGAGGGGCTGGGAATGGGTGAT,8.21062788839
ATCTTTATCGGTCTTAGCAAAGGCTTTG,30.1092205446
CGGGCCAGACTGGCCGAGACGGGTCGTT,11.0586722001
CAGCATCATGCCGTGATCGCCGGGAAAG,0.67958058668
GGGGAAAGGACAAGCAGTGCGGGCAAAA,29.2338752707
GAGAGAATTTTGACCTGATCCGGCTCGC,2.28311187737
CGTGATGCAACTGTGTAATGCGGCTGAC,27.8665335936
GAACATCACCGCCTCACGTCCGGTTTTG,26.3480104838
TCGATTGAGGGGCTGGGAATGGGTGATC,41.2590972746
CCGTGTAAGGGAGATTACACAGGCTAAG,4.25926295656
```


## 5: Validate the training of the model

This will assess whether the training model is working. It will not change the model used for predictions.


## 6: Data availability and processing

Raw sequence reads from which the datasets are derived are available at: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1260991

NCBI SRA BioProject: PRJNA1260991


## 7: Citations

* Guo, J. et al. Improved sgRNA design in bacteria via genome-wide activity profiling. Nucleic acids research **46**, 7052–7069 (2018).
* Abadi, M. et al. TensorFlow: Large-scale machine learning on heterogeneous systems (2015). Software available from tensorflow.org.
* Fernandes, A. D. et al. Unifying the analysis of high-throughput sequencing datasets: characterizing RNA-seq, 16S rRNA gene sequencing and selective growth experiments by compositional data analysis. Microbiome **2**, 1–13 (2014).
* Virtanen, P. et al. SciPy 1.0: fundamental algorithms for scientific computing in python. Nat. Methods **17**, 261–272 (2020).

## 8: How to cite crisprHAL

Ham, D.T., Browne, T.S., Banglorewala, P.N. et al. A generalizable Cas9/sgRNA prediction model using machine transfer learning with small high-quality datasets. **Nat Commun** *14*, 5514 (2023). https://doi.org/10.1038/s41467-023-41143-7
