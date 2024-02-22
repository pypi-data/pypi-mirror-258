import torch

class ModelProcess(object):
    def __init__(self) -> None:
        pass

    #key_replace_list = [(str, str),(str, str),(str, str), ...]
    def merge_model(self, model, path_src, path_merged, key_replace_list=None):
        checkpoint = torch.load(path_src)
        checkpoint_dict = dict(checkpoint.items())
        for mitemk, mitemv in torch.load(path_merged).items():
            if mitemk.split(".")[0] == "inst_head":
                mitemk = mitemk.replace("inst_head", "instance")
                checkpoint_dict.update({mitemk: mitemv})
            elif mitemk.split(".")[0] == "mask_head":
                mitemk = mitemk.replace("mask_head", "mask")
                checkpoint_dict.update({mitemk: mitemv})
        # for k ,v in checkpoint_dict.items():
        #     print(k)
        # print(checkpoint.items().append())
        model.load_state_dict(
            {k.replace('module.', ''): v for k, v in checkpoint_dict.items()})
        pass

    def show_keys(self, model):
        for key, v in model.cpu().state_dict().items():
            print(key)
    
    def auto_adapt(self, model, weight_path, strict=True): 
        new_weights = None
        new_weights = self.auto_remove_items(model, weight_path, strict)
        new_weights = self.auto_add_items(model, weight_path, strict)
        return new_weights

    def auto_remove_items(self, model, weight_path, strict=True):
        pretrained_weights = torch.load(weight_path, map_location=torch.device('cpu'))
        model.cpu()
        model_state_dict = model.state_dict()
        for key, value in pretrained_weights.items():
            if key not in model_state_dict:
                print("Del", key)
            else:
                model_state_dict[key] = value
                print("Skipping", key, "as it already exists")
        model.load_state_dict(model_state_dict, strict)
        return model

    def auto_add_items(self, model, weight_path, strict=True):
        pretrained_weights = torch.load(weight_path, map_location=torch.device('cpu'))
        model.cpu()
        model_state_dict = model.state_dict()
        for key, value in pretrained_weights.items():
            if key not in model_state_dict:
                print("Add", key)
                model_state_dict[key] = value
            else:
                print("Skipping", key, "as it already exists")
        model.load_state_dict(model_state_dict, strict)
        return model

    def remove_layer(self, model_loaded, layer_name, strict=True):
        model_state_dict = model_loaded.state_dict()
        if layer_name in model_state_dict.keys():
            del model_state_dict[layer_name]
        model_loaded.load_state_dict(model_state_dict, strict)
        return model_loaded