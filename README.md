# penny-pi

> *a small self driving robot that loves our cat named penny :)*

---

## current features

| Feature  | State |
| :--------------- | :-----: |
| Bluetooth Driving  | ✅  |
| Self Driving  | ✅  |
| Obstacle Avoidance  | ❌ |
| Cat Detection  | 🟡 |
| Tag Following  | ❌ |

## hardware

*none of the links work yet*

> * chasis: [todo](google.com)
> * "brain": [raspberry pi 2](google.com)
> * camera: [raspicam](google.com)
> * controller: [l298n](google.com)
> * lights: [generic GPIO lights](google.com)
> * speakers: [generic GPIO speakers](google.com)
> * bluetooth: [generic bluetooth USB](google.com)

## software

currently, we can just connect to it with SSH, after that, we just do the follwing:
```bash
#wherever penny-pi is located
python penny-pi/server.py

#now in a different terminal/tab
sudo rfcomm watch hci0
```
then, you are able to connect on a bluetooth pairing app. we just use one found on the app store, and to adjust the input values (ex: "A"-> go forward, "B"-> go backwards), you can just adjust the very top of the `server.py` file *(not implemented yet, you must scroll down in the code to do this)*

## machine learning

we gathered roughly 5k images total split evenly between the three classes `['F', 'L', 'R']` from the camera + normal bluetooth driving. once we recorded the data, we did a quick analysis of it through `npz-reader.py`, then ran it through a simple CNN. we got roughly `79%`, but it suprisingly worked really well.

the next part was pretty basic, you can find some of our models in `/machine-learning/`. once we train one, we then convert it into a `.tflite` file so it can run on the raspberry pi. afterwards, we just used the documentation to making a simple set up of inputing the pixel array from the image, and outputting what the model wants to do.

```
#predictions will print in the `python penny-pi/server.py` terminal like below
[0, 1, 0] <- go left
[1, 0, 0] <- go forwards
[0, 0, 1] <- go right
...
```
