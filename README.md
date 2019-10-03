# e-ink-bus-display
A bus stop schedule display made from rpi-zero and waveshare 2.7" e-ink screen

# Development flow

HOX, these are fish-scripts, if you use bash/zsh, feel free to change
the syntax accordingly :)

On your dev machine, inotifywait for changes and propagnate whem with
rsync to rpi:

```
while inotifywait -e close_write main.py ; rsync -a . raspi-zero-w-00:~/e-ink-bus-display ;  end
```

On rpi, wait for rsync to change the main.py:

```
while inotifywait -e open main.py ; sudo python main.py  ;  end
```

# Dependencies
