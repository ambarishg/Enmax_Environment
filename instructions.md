# Create a new resource group to hold the form recognizer resource
# if using an existing resource group, skip this step
az group create --name rgenmax --location eastus

# Create form recognizer
az cognitiveservices account create \
    --name enmaxextractor \
    --resource-group rgenmax \
    --kind FormRecognizer \
    --sku S0 \
    --location eastus \
    --yes

# Get the endpoint for the form recognizer resource
az cognitiveservices account show --name enmaxextractor --resource-group rgenmax --query "properties.endpoint"

https://eastus.api.cognitive.microsoft.com/

az cognitiveservices account keys list --name enmaxextractor --resource-group rgenmax

{
  "key1": "2aeb705af3124b42ba3535436c09dc49",
  "key2": "1a2bb5d780214653b01e78526ef4a98f"
}