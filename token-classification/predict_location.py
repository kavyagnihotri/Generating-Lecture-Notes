import torch
import os
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Example
text = "and sewage systemsTradesperson specializing in water and sewage systems mwparseroutput infoboxsubboxpadding0bordernonemargin3pxwidthautominwidth100fontsize100clearnonefloatnonebackgroundcolortransparent mwparseroutput infobox3colschildmarginauto mwparseroutput infobox navbarfontsize100body skinminerva mwparseroutput infoboxheaderbody skinminerva mwparseroutput infoboxsubheaderbody skinminerva mwparseroutput infoboxabovebody skinminerva mwparseroutput infoboxtitlebody skinminerva mwparseroutput infoboximagebody skinminerva mwparseroutput infoboxfulldatabody skinminerva mwparseroutput infoboxbelowtextaligncenterPlumber Residential plumber at work Occupation Occupation type Vocational Activity sectors Construction Description Education required Industrial Training Institute ITI Apprenticeship Related jobs Carpenter electricianPlumberPlumberResidential plumber at work Occupation Occupation type Vocational Activity sectors Construction Description Education required Industrial Training Institute ITI Apprenticeship Related jobs Carpenter electricianResidential plumber at work Residential plumber at work $IMG$ Residential plumber at work Residential plumber at work OccupationOccupationOccupationOccupation type VocationalOccupation typeOccupation typeOccupation typeVocationalVocationalVocationalActivity sectors ConstructionActivity sectorsActivity sectorsActivity sectorsConstructionConstructionDescriptionDescriptionDescriptionEducation required Industrial Training Institute ITI ApprenticeshipEducation requiredEducation requiredEducation requiredIndustrial Training Institute ITI ApprenticeshipIndustrial Training InstituteIndustrial Training Institute ITI ApprenticeshipApprenticeshipRelated jobs Carpenter electricianRelated jobsRelated jobsRelated jobsCarpenter electricianCarpenterCarpenter electricianelectrician A plumber is a tradesperson who specializes in installing and maintaining systems used for potable drinking water and for sewage and drainage in plumbing systems 1 2 A plumberplumber is a tradespersontradesperson who specializes in installing and maintaining systems used for potable drinking waterwater and for sewagesewage and drainagedrainage in plumbingplumbing systems 111222 History edit The origin of the word plumber dates from the Roman Empire 3 4 Roman roofs used lead in conduits and drain pipes 5 and some were also covered with lead lead was also used for piping and for making baths 6 The Latin for lead is plumbum In medieval times anyone who worked with lead was referred to as a plumber this can be seen from an extract about workmen fixing a roof in Westminster Palace they were referred to as plumbers To Gilbert de Westminster plumber working about the roof of the pantry of the little hall covering it with lead and about various defects in the roof of the little hall 7 Thus a person with expertise in working with lead was first known as a Plumbarius which was later shortened to plumber Plumbing activities edit Plumber exiting a sewer via a manhole Years of training andor experience are needed to become a skilled plumber some jurisdictions also require that plumbers be licensed Common plumbing tasks and skills include Reading drawings and specifications to determine the layout of water supply waste and venting systems Detecting faults in plumbing appliances and systems and correctly diagnosing their causes Installing repairing and maintaining domestic commercial and industrial plumbing fixtures and systems Locating and marking positions for pipe connections passage holes and fixtures in walls and floors Measuring cutting bending and threading pipes using hand and power tools or machines Joining pipes and fittings together using soldering techniques compression fittings threaded fittings solvent weld crimp and pushfit fittings Testing pipes for leaks using air or water pressure gauges Paying attention in all work undertaken to legal regulations and safety issues Ensuring that all safety standards and building regulations are met United States edit Each state and locality may have its own licensing and taxing schemes for plumbers Some states license journeymen and master plumbers separately while others license only master plumbers To become licensed plumbers must meet standards for training and experience and in most cases pass a certification exam 8 There is no federal law establishing licenses for plumbers 9 Canada edit In Canada licensing requirements differ by province however the provinces have pooled resources to develop an Interprovincial Program Guide that developed and now maintains apprenticeship training standards across all provinces The Red Seal Program formally known as the Interprovincial Standards Red Seal Program is a program that sets common standards to assess the skills of tradespeople across Canada 10 The Red Seal when affixed to a provincial or territorial trade certificate indicates that a tradesperson has demonstrated the knowledge required for the national standard in that trade United Kingdom edit National Vocational Qualifications NVQ remained the main form of plumbing qualification until they were superseded in 2008 by the Qualification and Credit Framework QCF 11 and then again in 2015 into the National qualifications frameworks in the United Kingdom The terms NVQ and SVQ Scottish Vocational Qualification are still widely used 12 Plumbers in the United Kingdom are required to pass Level 2 and Level 3 vocational requirements of the City and Guilds of London Institute"

# Directory
curr_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(curr_dir)
model_dir = os.path.join(parent_dir, 'models', 'image-location')

# Load model
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForTokenClassification.from_pretrained(model_dir)

# Split the input text into smaller parts
max_seq_length = 200  # Adjust this based on your model's maximum token limit
tokenized_texts = []
for i in range(0, len(text), max_seq_length - 2):  # Subtract 2 for [CLS] and [SEP] tokens
    chunk = text[i:i + max_seq_length - 2]
    input_ids = torch.tensor(tokenizer.encode(chunk)).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_ids)

    # Rid of [CLS] and [SEP] tokens (first and last)
    predictions = outputs[0].argmax(axis=-1)[0][1:-1]

    # Map label class indexes to string labels.
    for token, pred in zip(tokenizer.tokenize(text), predictions):
        print(token, ': ', model.config.id2label[pred.numpy().item()])


# # Get input for BERT
# input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)
# print(type(input_ids))

# # Predict
# with torch.no_grad():
#   outputs = model(input_ids)

# # From the output let's take the first element of the tuple.
# # Then, let's get rid of [CLS] and [SEP] tokens (first and last)
# predictions = outputs[0].argmax(axis=-1)[0][1:-1]

# # Map label class indexes to string labels.
# for token, pred in zip(tokenizer.tokenize(text), predictions):
#   print(token, '->', model.config.id2label[pred.numpy().item()])
