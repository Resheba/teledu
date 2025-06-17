from src.config import Texts


def sorted_chapters(texts: Texts) -> list[str]:
    return [
        data.strip()
        for _, value in sorted(
            [
                (k, v)
                for (k, v) in texts.education.model_dump(by_alias=True).items()
                if isinstance(v, dict)
            ],
            key=lambda x: x[1]["id"],
        )
        if (data := value.get("main_button_text")) is not None
    ]
