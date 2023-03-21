import os
import time
import torch
import numpy as np
import torch.backends.cudnn as cudnn
from argparse import ArgumentParser
# user
from builders.model_builder import build_model
from utils.utils import save_predict
import cv2
import pickle


def parse_args():
    parser = ArgumentParser(description='Efficient semantic segmentation')
    # model and dataset
    parser.add_argument('--model', default="ENet", help="model name: (default ENet)")
    parser.add_argument('--dataset', default="sweeper", help="dataset: sweeper")
    parser.add_argument('--num_workers', type=int, default=2, help="the number of parallel threads")
    parser.add_argument('--batch_size', type=int, default=1,
                        help=" the batch_size is set to 1 when evaluating or testing")
    parser.add_argument('--checkpoint', type=str,default="",
                        help="use the file to load the checkpoint for evaluating or testing ")
    parser.add_argument('--save_seg_dir', type=str, default="./server/",
                        help="saving path of prediction result")
    parser.add_argument('--cuda', default=True, help="run on CPU or GPU")
    parser.add_argument("--gpus", default="0", type=str, help="gpu ids (default: 0)")
    parser.add_argument("--predict_image", type=str, default="", help="image need to be test")
    args = parser.parse_args()

    return args

def predict_demo(args,model):
    
    model.eval()
    image = cv2.imread(args.predict_image, cv2.IMREAD_COLOR)
    name=str(args.predict_image).split('/')[2].split('.')[0]
    origin_path = os.path.join(args.save_seg_dir, name + '_origin.png')
    cv2.imwrite(origin_path,image)
    size = image.shape
    dim = (480,360)
    mean=pickle.load(open('./dataset/sweeper/new_inform.pkl', "rb"))['mean']
    image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    image = np.asarray(image, np.float32)

    image -= mean
    # image = image.astype(np.float32) / 255.0
    image = image[:, :, ::-1]  # revert to RGB
    image = image.transpose((2, 0, 1))  # HWC -> CHW
    input=image.copy()
    input = torch.from_numpy(input).unsqueeze(0)
    with torch.no_grad():
        if args.cuda:
            input_var = input.cuda()
        else:
            input_var = input
    T1 = time.time()
    output = model(input_var)
    T2 = time.time()
    print('inference time is %ss' % (T2 - T1))
    torch.cuda.synchronize()
    output = output.cpu().data[0].numpy()
    output = output.transpose(1, 2, 0)
    output = np.asarray(np.argmax(output, axis=2), dtype=np.uint8)
    # print(output)
    # output.completed = True
    save_predict(output, None, name, args.dataset, args.save_seg_dir,
                    output_grey=False, output_color=True, gt_color=False)



def test_model(args):
    """
     main function for testing
     param args: global arguments
     return: None
    """
    # print(args)

    if args.cuda:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpus
        if not torch.cuda.is_available():
            raise Exception("no GPU found or wrong gpu id, please run without --cuda")

    # build the model
    model = build_model(args.model, num_classes=args.classes)

    if args.cuda:
        model = model.cuda()  # using GPU for inference
        cudnn.benchmark = True

    if not os.path.exists(args.save_seg_dir):
        os.makedirs(args.save_seg_dir)

    if args.checkpoint:
        if os.path.isfile(args.checkpoint):
            checkpoint = torch.load(args.checkpoint)
            model.load_state_dict(checkpoint['model'])
        else:
            raise FileNotFoundError("no checkpoint found at '{}'".format(args.checkpoint))

    predict_demo(args,model)


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('g'):
                fullname = os.path.join(root, f)
                yield fullname

if __name__ == '__main__':

    args = parse_args()
    if args.dataset == 'sweeper':
        args.classes = 4
    else:
        raise NotImplementedError(
            "This repository now supports sweeper datasets, %s is not included" % args.dataset)
    predict_base = './example_image'
    model = ['CGNet']
    # model = ['ERFNet']
    for i in model:
        args.model=i
        args.checkpoint='./checkpoint/sweeper/'+i+'bs8gpu1_train/model_191.pth'

        args.save_seg_dir = './server/'
        args.save_seg_dir = os.path.join(args.save_seg_dir, args.dataset, 'predict', args.model)
        for j in findAllFile(predict_base):
            args.predict_image='./example_image/'+j.split('/')[-1]
            test_model(args)
        # args.predict_image = './example_image/frame0330.jpg'
        # test_model(args)
