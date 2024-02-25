import torch
from torchvision import models, transforms
from torchvision.transforms.functional import to_pil_image

def get_result(img, model_name='resnet18', num_classes=10):
    # 모델 불러오기
    model = getattr(models, model_name)(pretrained=True)
    
    # 모델 구조 수정
    if model_name in ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']:
        num_ftrs = model.fc.in_features
        model.fc = torch.nn.Linear(num_ftrs, num_classes)
    elif model_name in ['vgg16', 'vgg19']:
        num_ftrs = model.classifier[6].in_features
        model.classifier[6] = torch.nn.Linear(num_ftrs, num_classes)
    else:
        raise ValueError('Invalid model name')
    
    model.eval()  # 모델을 평가 모드로 설정
    
    # 이미지 변환 파이프라인 정의
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # 많은 모델들에서 흔히 사용되는 크기
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    # 이미지 전처리
    img = to_pil_image(img)
    img = transform(img)
    img = img.unsqueeze(0)  # 배치 차원 추가
    
    # 이미지 분류
    with torch.no_grad():
        outputs = model(img)
        _, predicted = torch.max(outputs, 1)
        return predicted.item()
