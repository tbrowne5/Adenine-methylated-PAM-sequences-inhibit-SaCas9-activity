import sys
import os
from model import models, modelVersionDefaultEpochs
from processing import processing

training = False
modelName = "TEVSACAS9"
modelNames = ["TEVSACAS9","SACAS9","TEVSACAS","TEVCAS9","SACAS"]
epochs = None
inputFile = None
outputFile = None
compare = False
circularInput = False
summary = False

# PERHAPS MOVE THIS TO PROCESSING AND HAVE A VERY SIMPLE CRISPRHAL.PY FILE!!!

def parse_args(args):
    global training, modelName, modelNames, epochs, inputFile, outputFile, compare, circularInput, summary

    for i in range(len(args)):
        if args[i] == "--train" or args[i] == "-t": training = True
        elif args[i] == "--input" or args[i] == "-i": inputFile = args[i + 1]
        elif args[i] == "--output" or args[i] == "-o": outputFile = args[i + 1]
        elif args[i] == "--circular": circularInput = True
        elif args[i] == "--compare" or args[i] == "-c": compare = True
        elif args[i] == "--epochs" or args[i] == "-e": epochs = int(args[i + 1])
        elif args[i] == "--summary" or args[i] == "-s": summary = True
        elif args[i] == "--model" or args[i] == "-m" or args[i] == "--enzyme":
            if args[i + 1].upper() in ["TEVSACAS9","SACAS9","TEVSACAS","TEVCAS9","SACAS"]: modelName = "TEVSACAS9"
            else:
                print(f"Error: Model '{args[i + 1]}' is not recognized. Available model is: SaCas9, for more models please use: github.com/tbrowne5/crisprHAL")
                sys.exit(1)
        elif args[i] == "--help" or args[i] == "-h":
            print("Usage: python crisprHAL.py [options]")
            print("Options:")
            print("  --input, -i   [Input file path]             Input file for prediction (fasta, csv, or tsv)")
            print("  --output, -o  [Output file path]            Output file for prediction results")
            print("  --circular                                  Process fasta as a circular input sequence")
            print("  --compare, -c                               Compare predictions with scores in the input file second column")
            print("  --train, -t                                 Train the model specified")
            print("  --epochs, -e  [Integer epoch value]         Specify number of epochs for training (default: model-specific)")
            print("  --summary, -s                               Print the model architecture summary")
            print("  --help, -h                                  Show this help message")
            sys.exit(0)
    
    if training == True and inputFile is not None:
        print("Error: Please specify either training mode or an input file for prediction generation.")
        sys.exit(1)

# Read in arguments
# If no input specified, use default hold-out test set
# If no output specified, but input specified, strip file type annd add _predictions.csv

def run_model():
    global training, modelName, inputFile, outputFile, compare, epochs, circularInput, summary

    process = processing()
    model = models(modelName, summary)
    
    if training:
        print("Training model")
        trainingData = process.read_training_data(modelName)
        testingData = process.read_testing_data(modelName)
        if epochs is None: epochs = modelVersionDefaultEpochs[modelName]
        for i in range(0,epochs):
            model.train(trainingData[1], trainingData[2], epochs=1, batch_size=1024, verbose=1)
            process.compare_predictions(model.predict(testingData[1]), testingData[2], message=f"Epoch {i+1} on hold-out test set for {modelName}:")
    else:
        # Model name provides input sequence length for processing
        # If inputFile default of "None" is passed, the hold-out test set will be used instead
        # The compare flag indicates that the input file contains a second column of scores to be used for comparison
        if inputFile is None: compare = True
        print(f"{modelName} {inputFile} {compare} {circularInput}")
        inputSequences, encodedInputSequences, inputScores = process.read_input(modelName, inputFile, compare, circularInput)
        print(len(inputSequences))
        print(encodedInputSequences.shape)
        model.load_model(modelName)
        predictions= model.predict(encodedInputSequences)
        #print(predictions.shape)
        print(outputFile)
        print(inputFile)
        if compare:
            # Compare predictions with the second column of scores in the input file
            process.compare_predictions(predictions, inputScores)
        process.write_predictions(inputSequences, predictions, outputFile, inputFile, inputScores)

if __name__ == "__main__":
    print("\nWelcome to crisprHAL SaCas9 — Adenine methylated PAM sequences inhibit SaCas9 activity\n\nPlease be aware that this is a static repository specific to the paper, and as such may not contain up-to-to date models.\n\nThe production models can be found at github.com/tbrowne5/crisprHAL or online at crisprHAL.streamlit.app — thank you!")
    parse_args(sys.argv[1:])
    run_model()
