# pixel_comparison
Recognize image by comparing pixels

## Create Examples by
1. Hand write numbers 8x8 pixels. Save each file as x.n.png format. x = number, n = the # of the number 
2. Make a **root path**. Save the images under it.
3. Create a test.png file (also 8x8 pixels.png). Save under a **certain path**

In the example:
* root path = images\numbers\
* certain path = images\numbers\test.png

## Run model
1. If no img.db has ever been created
```
createExamples()
```
2. Run model.py
```
whatNumIsThis('images/numbers/test.png')
```

## Output
eg. put a 6.n.png:
![alt text](Figure_1.png)
