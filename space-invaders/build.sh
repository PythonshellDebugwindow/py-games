[ -d "build" ] && rm -r build
python convert_to_exe.py build
BD=$(echo build/*)
cp -r assets $BD/assets
mkdir $BD/engine
cp -r engine/engine_assets $BD/engine/engine_assets
