## Template replace

A little script for substituting fields in form letters, so you stop sending mails with the wrong name. Use `run.py -h` to see all options.

Template should look like:

```
Dear {{name}},

I am sending you this e-mail because you like {{food-item}}.

Best,
{{sender}}
```

Another csv file (defaults to tab separated) containing the replacement values. Ie.

```
name<TAB>food-item<TAB>sender
Cookie Monster<TAB>cookies<TAB>Cookie Corp.
Elmo<TAB>Being Loud<TAB>Downstairs Neighbours
```

Results in:
```
Dear Cookie Monster,

I am sending you this e-mail because you like cookies.

Best,
Cookie Corp.
```
