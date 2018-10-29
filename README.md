# Wox-Dash-Zeal

need to install python, zeal (https://zealdocs.org/) and some docsets for zeal.

## config

### docspath

The path to zeal's dossets path:

```json
{
    "path": "D:\\Program Files\\Zeal\\dossets"
}
```

## alias help

```
z ~help
```

### set query alias

```
z ~set py3=python3
```

### del query alias

```
z ~del py3
```

### list query alias

```
z ~list
```

## use

```
z py3:sys.v
```

```
z py2,py3:sys.v
```

```
z rust,c:print
```

```
z rust:alloc:
z rust:alloc::
z rust:alloc::fmt
```

