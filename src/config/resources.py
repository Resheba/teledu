from pydantic import BaseModel, Field


class Form(BaseModel):
    text: str
    video_id: str | None = None


class Registration(BaseModel):
    image_id: str
    form_1: Form
    form_2: Form
    form_3: Form
    form_4: Form


class EduBase(BaseModel):
    id: int
    main_button_text: str


class Edu1(EduBase):
    delay_sec: float
    form_1: Form
    form_2: Form
    form_3: Form
    form_4: Form
    form_5: Form
    form_6: Form
    form_7: Form
    form_8: Form


class Edu2(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu3(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu4(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form
    form_4: Form
    form_5: Form
    form_6: Form
    form_7: Form
    form_8: Form
    form_9: Form
    form_10: Form
    form_11: Form
    form_12: Form
    form_13: Form
    form_14: Form
    form_15: Form
    form_16: Form


class Edu5(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu6(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu7(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu8(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu9(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu10(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu11(EduBase):
    form_1: Form
    form_2: Form
    form_3: Form


class Edu12(EduBase):
    form_1: Form


class Education(BaseModel):
    next_button_text: str
    watch_button_text: str

    edu1: Edu1 = Field(alias="1")
    edu2: Edu2 = Field(alias="2")
    edu3: Edu3 = Field(alias="3")
    edu4: Edu4 = Field(alias="4")
    edu5: Edu5 = Field(alias="5")
    edu6: Edu6 = Field(alias="6")
    edu7: Edu7 = Field(alias="7")
    edu8: Edu8 = Field(alias="8")
    edu9: Edu9 = Field(alias="9")
    edu10: Edu10 = Field(alias="10")
    edu11: Edu11 = Field(alias="11")
    edu12: Edu12 = Field(alias="12")

    @property
    def all(self) -> tuple[EduBase, ...]:
        return (
            self.edu1,
            self.edu2,
            self.edu3,
            self.edu4,
            self.edu5,
            self.edu6,
            self.edu7,
            self.edu8,
            self.edu9,
            self.edu10,
            self.edu11,
            self.edu12,
        )


class Documents(BaseModel): ...


class Exam(BaseModel):
    next_button_text: str
    form_1: Form
    form_2: Form
    form_3: Form
    form_4: Form


class Texts(BaseModel):
    registration: Registration
    education: Education
    documents: Documents
    exam: Exam

    def __hash__(self) -> int:
        return 1
