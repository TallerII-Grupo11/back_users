# back_users


[![codecov](https://codecov.io/gh/TallerII-Grupo11/back_users/branch/main/graph/badge.svg?token=X5YSLG3P2G)](https://codecov.io/gh/TallerII-Grupo11/back_users)
[![Linters](https://github.com/TallerII-Grupo11/back_users/actions/workflows/linter.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_users/actions/workflows/linter.yaml)
[![Tests](https://github.com/TallerII-Grupo11/back_users/actions/workflows/test.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_users/actions/workflows/test.yaml)
[![Deploy](https://github.com/TallerII-Grupo11/back_users/actions/workflows/deploy.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_users/actions/workflows/deploy.yaml)

### Documentation

http://spotifiuby-back-users.herokuapp.com/docs

### Dependencies

- Python 3.9
- Poetry


### Test

Run tests using [pytest](https://docs.pytest.org/en/6.2.x/)

``` bash
pytest tests/
```


### Docker

``` bash
docker build -t back-users:0.1 .
docker run -p 5000:5000 --env-file .env back-users:0.1
```


### Manual Deploy to Heroku

``` bash
heroku container:push web -a <HEROKU-APP-NAME>
heroku container:release web -a <HEROKU-APP-NAME>
```

If using Apple M1 chip, build locally and push with:
```bash
docker buildx build --platform linux/amd64 -t back-users:0.1 .
docker tag back-users:0.1 registry.heroku.com/<HEROKU-APP-NAME>/web
docker push registry.heroku.com/<HEROKU-APP-NAME>/web
```

and then release:
``` bash
heroku container:release web -a <HEROKU-APP-NAME>
```



### Resources

- https://devcenter.heroku.com/articles/build-docker-images-heroku-yml
- https://devcenter.heroku.com/articles/container-registry-and-runtime
- https://stackoverflow.com/questions/66982720/keep-running-into-the-same-deployment-error-exec-format-error-when-pushing-nod
