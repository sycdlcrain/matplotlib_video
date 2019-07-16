Create a video in python using matplotlib

1. run a script that generates a plot
```bash
python use_pid_class.py
```
2. cd into the video folder
```bash
cd video
```
3. convert the still images into a movie
```bash
ffmpeg -r 10 -i %d.png my_movie.mp4
```
4. clean up
```bash
rm *.png
```