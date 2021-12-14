# Mocki API Feed

[Mocki docs](https://mocki.io/docs)  

Base URL:  
api.mocki.io/v2/d3d81fe1

<hr>

### Mocki API compilation instructions

To compile a new version of config.yml first add the required JSON files to the `data_mocki` directory and then run:

```bash
docker-compose run --rm app python process_mocki.py
```

Commit and push the changes to the github repo, the API endpoints will now be available at:

```
[base_url]/[json_file_name]
```

e.g.
`https://api.mocki.io/v2/d3d81fe1/30119-mens-loafers`

### External data processing instructions

1. Copy json data files into the `data_ext` folder
2. Run `docker-compose run --rm app python process_external.py`
3. Wait for process to complete, then copy modified files back to Avoir repo
4. Delete json files in the `data_ext` folder
```
