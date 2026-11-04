# Ancient Civilization — Prototype 0.1

Windows prototype using Python + Kivy.

## Install
Open CMD in this folder:

```bat
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install "kivy[base]"
```

## Run
```bat
python main.py
```

## Controls
- Hold and drag the left mouse button: move around the map.
- Mouse wheel: zoom.
- Click a tree: get 5 wood (uses 1 axe charge).
- Click a rock: get 4 stone (uses 1 pickaxe charge).
- Click "Строить", then click a free map location.
- "Сменить здание" switches between a house and a shop.
- Houses increase population capacity. Residents arrive periodically.
- Shops periodically generate money.
- Port, railway station and airport are visible from the start and unlock at levels 10, 15 and 30.

This is an early prototype, not the complete game. Saving, quests, real repairs, trade and transport deliveries
will be added in later versions. The current graphics are placeholder shapes.
