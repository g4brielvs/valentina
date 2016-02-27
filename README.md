# Valentina

## Building assets

`bower` and `sass` commands are required to generate CSS assets:

```console
$ bower install
$ sass valentina/home/static/css/main.sass valentina/core/static/css/main.css
```

Alternatively you can set a watcher:

```console
sass --watch valentina/home/static/css/main.sass:valentina/home/static/css/main.css
```