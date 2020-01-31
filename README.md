# reddit-transtool

This is a tool for crawling reddit post, for translating them.

As of now it can crawl the comments of a post and print it out the console.

-----

## Instruction

### Set up dependencies

```bash
$ pip install -r requirements.txt
```

### Run the app locally

For Linux and Mac:

```bash
$ export FLASK_APP=crawler
$ export FLASK_ENV=development
$ flask run
```

For Windows cmd:

```shell
> set FLASK_APP=crawler
> set FLASK_ENV=development
> flask run
```

For Windows Powershell:

```shell
$env:FLASK_APP=crawler
$env:FLASK_ENV=development
flask run
```


For more details, please refer to the
[official document](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)
