# utils/image_captionner.py

import boto3
import json
from botocore.exceptions import ClientError

# AWS Bedrock client (region must match your model's availability)
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Model mapping (can be extended later)
MODEL_IDS = {
    "claude-3.5-sonnet-v1": "anthropic.claude-3-5-sonnet-20240620-v1:0"
}

# Prompt for high-end fashion description
FASHION_PROMPT = (
    "You are a professional high-end fashion designer with expertise in luxury garment analysis. "
    "You are reviewing a product photo from a premium fashion catalog for archival documentation. "
    "\n\n"
    "Analyze and describe the garment with expert precision, including:\n"
    "• Precise dimensions and proportions (length, fit, cut, silhouette)\n"
    "• Fabric composition, texture, and weight\n" 
    "• Construction details (stitching, seaming, finishing)\n"
    "• Color palette and tonal variations\n"
    "• Style influences and design references\n"
    "• Notable design features, embellishments, or hardware\n"
    "• Seasonal appropriateness and styling versatility\n"
    "\n"
    "Write in a concise yet sophisticated tone appropriate for a high-end fashion lookbook "
    "or design archive. Focus on technical accuracy and industry-standard terminology."
)


def caption_image(image_base64: str, model_key: str) -> str:
    """
    Generates a fashion-oriented caption for an image using AWS Bedrock Claude.
    
    Args:
        image_base64 (str): Base64-encoded image data.
        model_key (str): Key from MODEL_IDS dict (e.g., 'claude-3.5-sonnet-v1').

    Returns:
        str: Generated caption.
    """
    if model_key not in MODEL_IDS:
        raise ValueError(f"Model '{model_key}' not found. Available: {list(MODEL_IDS.keys())}")

    model_id = MODEL_IDS[model_key]

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.3,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_base64}},
                    {"type": "text", "text": FASHION_PROMPT}
                ],
            }
        ],
    }

    try:
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(native_request)
        )

        model_response = json.loads(response["body"].read())
        caption = model_response["content"][0]["text"].replace("\n", " ")
        return caption

    except ClientError as e:
        raise RuntimeError(f"AWS Client error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")
