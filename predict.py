import os
from tempfile import TemporaryDirectory as tmpdir

import magic
from bg_remove import BGRemove
from cog import BasePredictor, Input, Path


class Predictor(BasePredictor):
    def setup(self):
        print("setup")
        self.bgremover = BGRemove("/modnet_webcam_portrait_matting.ckpt")

    def predict(self, 
        image: Path = Input(description="input image"),
        ) -> Path:
        image = str(image)
        # get mimetype
        mime = magic.from_file(image, mime=True)
        
        # copy file to filename with correct extension for any type of image
        # we should change the backend to not give filenames without an extension in the future
        desired_extension = mime.split("/")[1]
        new_filename = image + "." + desired_extension
        os.system(f"cp \"{image}\" \"{new_filename}\"")
        image = new_filename
        
        print("running bgremover on image ", str(image))
        output_path = tmpdir().name
        self.bgremover.image(str(image), background=False, output=output_path)
        #os.system("ls -l /outputs")
        os.system(f"mv {output_path}/*.png {output_path}/output.png")
        return Path(f"{output_path}/output.png")

