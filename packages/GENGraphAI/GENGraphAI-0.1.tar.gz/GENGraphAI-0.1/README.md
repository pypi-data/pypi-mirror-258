## GENGraphAI

>  This library is designed for the generation of knowledge graphs from unstructured data using Vertex AI from Google Cloud as the LLM engine.
## About The Project

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

You need to make sure you have installed the following modules.
* Requests
  ```s
  pip install --user google-cloud-aiplatform
  ```
  ```s
  pip install --user google.cloud
  ```
  ```s
  pip install spacy
  ```
  ```s
  pip install --user neo4j
  ```
  ```s
  pip install --user langchain
  ```
  
### Installation

```python
pip install GENGraphAI
```

<!-- USAGE EXAMPLES -->
## Usage

* Example 1
    ```python
    import GENGraphAI
    import vertexai
    from langchain.graphs import Neo4jGraph
    from vertexai.preview.language_models import TextGenerationModel
    import spacy


    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="YOUR_API_KEY_HERE.json" # your api key
    nlp = spacy.load("es_core_news_sm") # Load data set
    host = "bolt://________________" # Direction of your project in neo4j sandbox
    user = "neo4j"
    password= "_________________" # Sandbox project password
    url="data.txt"  # Data format txt

    archivo = GENGraphAI.data_txt(url)

    graph = Neo4jGraph(
        url=host,
        username=user,
        password=password
    )

    fragmentos = GENGraphAI.dividir_en_fragmentos(archivo)
    project_id = '__________'
    location = 'us-central1' 
    vertexai.init(project=project_id, location=location)
    
    # Methods for google-cloud-aiplatform extraction
    def extract_entities_relationships(prompt, tuned_model_name=None):
    try:
        #res = run_text_model(project_id, "text-bison@001", 0, 1024, 0.8, 40, prompt, location, tuned_model_name)
        res = run_text_model(project_id, "text-bison-32k ", 0.3, 8192, 0.8, 40, prompt, location, tuned_model_name)
        return res
    except Exception as e:
        print(e)


    def run_text_model(
        project_id: str,
        model_name: str,
        temperature: float,
        max_decode_steps: int,
        top_p: float,
        top_k: int,
        prompt: str,
        location: str = location,
        tuned_model_name: str = "",
        ) :
        """Text Completion Use a Large Language Model."""
        vertexai.init(project=project_id, location=location)
        model = TextGenerationModel.from_pretrained(model_name)
        if tuned_model_name:
          model = model.get_tuned_model(tuned_model_name)
        response = model.predict(
            prompt,
            temperature=temperature,
            max_output_tokens=max_decode_steps,
            top_k=top_k,
            top_p=top_p,)
        return response.text

    graph.query("MATCH (n) DETACH DELETE n")

      
    GENGraphAI.una_extracion(extract_entities_relationships, fragmentos[0],graph) # Method for extracting a single fragment
    #GENGraphAI.extracion_completa(extract_entities_relationships, fragmentos, graph) # Method for complete extraction of the fragment text
    #GENGraphAI.extracion_emb(extract_entities_relationships, fragmentos[0], graph,nlp) # Method for extracting a single fragment with embedding
    ```
<!-- LICENSE -->
## License
