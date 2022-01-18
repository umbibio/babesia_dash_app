# Babesia Dashboard App

This repository contains the code for the Dashboard app corresponding to this publication:

Yasaman Rezvani*, Caroline D Keroack*, Brendan Elsworth, Argenis Arriojas, Marc-Jan Gubbels, Manoj T Duraisingh, Kourosh Zarringhalam, "Single cell transcriptional atlas of Babesia species reveals coordinated progression of transcriptomes and identifies conserved and species-specific transcriptional profiles", 2022, BioRxiv

You can find a live version [here](https://umbibio.math.umb.edu/babesiasc/)

### Setup
This should work on a linux based system with docker and docker-compose installed.
- Clone the repository
- Modify `docker-compose.yml` file to update the passwords
- Download the tsv data files from [this link](https://umbibio.math.umb.edu/data/babesia/tsv_files.tar.gz)
    - Extract tsv files and place them in the `./app/data/tsv_files` folder.
- Prepare and start the database container. This step may take several minutes to load the data into the database.
    - `$ docker-compose up db`
- Once the database is ready, you may start the dashboard app
    - `$ docker-compose up app`
- Visit the app on your web browser at http://localhost:8052/babesiasc/
