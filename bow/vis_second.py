import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import preprocess_input

from vis.utils import utils
from vis.utils.vggnet import VGG16
from vis.visualization import visualize_saliency

# Build the VGG16 network with ImageNet weights
model = VGG16(weights='imagenet', include_top=True)
print('Model loaded.')

# The name of the layer we want to visualize
# (see model definition in vggnet.py)
layer_name = 'predictions'
layer_idx = [idx for idx, layer in enumerate(model.layers) if layer.name == layer_name][0]

# Images corresponding to tiger, penguin, dumbbell, speedboat, spider
image_paths = [
"http://imagenesfotos.com/wp-content/2009/05/picasso-18.jpg",
"http://imagenesfotos.com/wp-content/2009/05/picasso-24.jpg",
"https://userscontent2.emaze.com/images/1dfc27f4-762a-428f-8041-d2cd575dd61e/45339e36e05039a775268784984e2aeb.jpg",
"http://3.bp.blogspot.com/-neTRjqu1GrI/UtS0W4cmfII/AAAAAAAACYU/Zpqb8a1yiPU/s1600/3.jpg"    
]

heatmaps = []
for path in image_paths:
    seed_img = utils.load_img(path, target_size=(224, 224))
    x = np.expand_dims(img_to_array(seed_img), axis=0)
    x = preprocess_input(x)
    pred_class = np.argmax(model.predict(x))

    # Here we are asking it to show attention such that prob of `pred_class` is maximized.
    heatmap = visualize_saliency(model, layer_idx, [pred_class], seed_img)
    heatmaps.append(heatmap)

plt.axis('off')
plt.imshow(utils.stitch_images(heatmaps))
#plt.title('Saliency map')
plt.show()
plt.savefig('myfig')
