# Con virtualenv
#python3.10 -m venv .venv
#source .venv/bin/activate
#crewai crewai-tools 

# Con conda
conda create --name gifted-children-helper python=3.10
conda activate gifted-children-helper
pip install -r requirements.txt

# reset memories
crewai reset-memories -a
rm ./db/chroma.sqlite3

sudo apt-get install wkhtmltopdf pdftotext

# covert pdf2text
pdftotext -layout 'TerapiaCognitivoConductualAplicadaANinosYAdolescdentes.pdf' 'TerapiaCognitivoConductualAplicadaANinosYAdolescdentes.txt'

# increase parameteer
   ollama show --modelfile snowflake-arctic-embed2  > ModelFile-snowflake-arctic-embed2
   echo 'PARAMETER num_ctx 4096' >> ModelFile-snowflake-arctic-embed2
   ollama create  snowflake-arctic-embed2-4k -f ModelFile-snowflake-arctic-embed2


   ollama show --modelfile qwen2.5:72b  > ModelFile
   echo 'PARAMETER num_ctx 8192' >> ModelFile
   ollama create  qwen2.5:72b-8k -f ModelFile

   ollama show --modelfile llama3.1:8b  > ModelFile
   echo 'PARAMETER num_ctx 8192' >> ModelFile
   ollama create  llama3.1:8b-8k -f ModelFile

   ollama show --modelfile qwen2.5:32b  > ModelFile
   echo 'PARAMETER num_ctx 8192' >> ModelFile
   ollama create  qwen2.5:32b-8k -f ModelFile

   ollama show --modelfile qwen2.5:14b  > ModelFile
   echo 'PARAMETER num_ctx 8192' >> ModelFile
   ollama create  qwen2.5:14b-8k -f ModelFile


Informe psicológico detallado muy profesional en markdown,incluyendo:
Informe neurológico muy profesional en markdown, incluyendo:
Informe de terapia ocupacional muy profesional en markdown, incluyendo:
Informe psicopedagógico muy profesional en markdown, incluyendo:
Informe de terapia familiar

Informe psicológico detallado 
Informe neurológico
Informe de terapia ocupacional
Informe psicopedagógico
Informe de terapia familiar