from datetime import datetime

from backend.models.response.news import NewsItem
from backend.settings import MongoConnectionDetails


class NewsService:
    def __init__(self, mongo_config: MongoConnectionDetails):
        self.mongo_config = mongo_config

    async def get_news(self, limit: int = None) -> list[NewsItem]:
        mock_tech_news = [
            {
                "id": "1",
                "title": "OpenAI Releases GPT-5",
                "content": "OpenAI has released GPT-5 with groundbreaking capabilities in reasoning and memory.",
                "source": ["https://openai.com/blog/gpt-5"],
                "publishedAt": datetime.now(),
                "category": "technology",
                "image": "https://developer-blogs.nvidia.com/wp-content/uploads/2020/07/OpenAI-GPT-3-featured-image.png",
            },
            {
                "id": "2",
                "title": "Apple Unveils New M4 Chip",
                "content": "Apple's new M4 chip sets a new benchmark in energy-efficient performance for laptops.",
                "source": [
                    "https://www.apple.com/newsroom/2025/05/apple-unveils-m4-chip/"
                ],
                "publishedAt": datetime.now(),
                "category": "technology",
                "image": "https://developer-blogs.nvidia.com/wp-content/uploads/2020/07/OpenAI-GPT-3-featured-image.png",
            },
            {
                "id": "3",
                "title": "Google Introduces AI-Powered Search",
                "content": "Google Search now features fully generative AI answers and contextual understanding.",
                "source": ["https://blog.google/products/search/generative-ai/"],
                "publishedAt": datetime.now(),
                "category": "technology",
                "image": "https://developer-blogs.nvidia.com/wp-content/uploads/2020/07/OpenAI-GPT-3-featured-image.png",
            },
            {
                "id": "4",
                "title": "Meta Launches New VR Headset",
                "content": "Meta's Quest 4 headset pushes the boundaries of virtual reality with retinal resolution.",
                "source": ["https://about.fb.com/news/2025/05/meta-quest-4-launch/"],
                "publishedAt": datetime.now(),
                "category": "technology",
                "image": "https://meta.com/images/quest-4.jpg",
            },
            {
                "id": "5",
                "title": "NVIDIA Announces Next-Gen GPUs",
                "content": "NVIDIA's H200 series GPUs promise faster AI training and inference at lower power.",
                "source": ["https://nvidia.com/en-us/news/next-gen-gpus/"],
                "publishedAt": datetime.now(),
                "category": "technology",
                "image": "https://nvidia.com/images/h200-gpu.png",
            },
            {
                "id": "6",
                "title": "Tesla Debuts Self-Driving Software v12",
                "content": "Tesla’s Full Self-Driving (FSD) v12 enters wide release with significant improvements.",
                "source": ["https://www.tesla.com/blog/fsd-v12-update"],
                "publishedAt": datetime.now(),
                "category": "technology",
                "image": "https://tesla.com/images/fsd-v12.png",
            },
            {
                "id": "7",
                "title": "Amazon Launches AI Shopping Assistant",
                "content": "Amazon introduces an AI assistant that helps users make personalized purchase decisions.",
                "source": ["https://amazon.com/news/ai-shopping-assistant"],
                "publishedAt": datetime.now(),
                "category": "technology",
                "image": "https://amazon.com/images/ai-assistant.jpg",
            },
            {
                "id": "8",
                "title": "Microsoft Rolls Out CoPilot for Office",
                "content": "Microsoft integrates AI-powered CoPilot into Word, Excel, and PowerPoint for productivity boost.",
                "source": [
                    "https://blogs.microsoft.com/blog/2025/05/copilot-for-office/"
                ],
                "publishedAt": datetime.now(),
                "category": "technology",
                "image": "https://microsoft.com/images/copilot-office.jpg",
            },
        ]
        return [NewsItem(**news) for news in mock_tech_news]
