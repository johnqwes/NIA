from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class ProjectModel(db.Model):
    __tablename__ = "sample"

    id = db.Column(db.Integer, primary_key=True)
    name_of_cis = db.Column(db.String(100))
    location = db.Column(db.String(100))
    source_of_water = db.Column(db.String(100))
    scheme_of_irrigation = db.Column(db.String(100))
    service_area = db.Column(db.Float)
    firmed_up_service_area = db.Column(db.Float)
    operational_area = db.Column(db.Float)
    num_farmer_beneficiaries = db.Column(db.Integer)
    name_of_ia = db.Column(db.String(100))
    main_canals = db.Column(db.String(100))
    laterals = db.Column(db.String(100))

    def __init__(self, name_of_cis, location,source_of_water,scheme_of_irrigation,service_area,firmed_up_service_area,operational_area,num_farmer_beneficiaries,name_of_ia,main_canals,laterals):
        self.name_of_cis = name_of_cis
        self.location = location
        self.source_of_water = source_of_water
        self.scheme_of_irrigation = scheme_of_irrigation
        self.service_area = service_area
        self.firmed_up_service_area = firmed_up_service_area
        self.operational_area = operational_area
        self.num_farmer_beneficiaries = num_farmer_beneficiaries
        self.name_of_ia = name_of_ia
        self.main_canals = main_canals
        self.laterals = laterals

        def __repr__(self):
            return f"{self.name_of_cis}:{self.location}"



