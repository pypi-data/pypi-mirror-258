from dataclasses import dataclass


@dataclass
class RelationKey:
    medical_institution_code: str
    medical_record_no: str
    discharge_time: str

    def __repr__(self):
        return '<RelationKey [机构代码：%s， 病案号：%s，出院时间：%s]>' % (self.medical_institution_code, self.medical_record_no, self.discharge_time)