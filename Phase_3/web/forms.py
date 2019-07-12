from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class CustomerSearchForm(FlaskForm):
    customer_types = ["Individual", "Business"]
    state = SelectField(label='Customer type', choices=customer_types)
    identification = StringField(label="Driver license or Business TIN", validators=[DataRequired()])
    
    submit = SubmitField("Search")

class VehicleForm(FlaskForm):
    vin = StringField(label="VIN", validators=[DataRequired()])
    manufacturer_name = SelectField(label="Manufacturer", validators=[DataRequired()], id="selected_manufacturer")
    vehicle_type = SelectField(label="Vehicle type", validators=[DataRequired()], id="selected_vehicle_type")
    model_year = SelectField(label="Model year", validators=[DataRequired()], id="selected_model_year")
    model_name = StringField(label="Model name", validators=[DataRequired()])
    mileage = FloatField(label="Mileage", validators=[DataRequired()])
    vehicle_condition = SelectField(label="Condition", validators=[DataRequired()], id="selected_condition")
    vehicle_description = StringField(label="Description", validators=[DataRequired()])
    kbb_value = FloatField(label="KBB value", validators=[DataRequired()])
    color = SelectMultipleField(label="Color", validators=[DataRequired()])
    customer = StringField(label="Customer ID", validators=[DataRequired()])

    submit = SubmitField("Finish Purchase")

class IndividualForm(FlaskForm):
    phone_number = StringField("Phone number", validators=[DataRequired()])
    email = StringField("Email address")
    street = StringField("Street", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    postal_code = StringField("Postal code", validators=[DataRequired()])

    driver_license_number = StringField("Driver license number", validators=[DataRequired()])
    individual_first_name = StringField("First name", validators=[DataRequired()])
    individual_last_name = StringField("Last name", validators=[DataRequired()])

class BusinessForm(FlaskForm):
    phone_number = StringField("Phone number", validators=[DataRequired()])
    email = StringField("Email address")
    street = StringField("Street", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    postal_code = StringField("Postal code", validators=[DataRequired()])

    tax_id_number = StringField("Business tax ID", validators=[DataRequired()])
    business_name = StringField("Business name", validators=[DataRequired()])
    pc_name = StringField("Primary contact name", validators=[DataRequired()])
    pc_title = StringField("Primary contact title", validators=[DataRequired()])
    
    submit = SubmitField("Save")

class VendorForm(FlaskForm):
    vendor_name = StringField("Vendor name", validators=[DataRequired()])
    vendor_phone_number = StringField("Phone number", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    postal_code = StringField("Postal code", validators=[DataRequired()])
    submit = SubmitField("Save")

class RepairForm(FlaskForm):
    repair_start_date = DateField("Start date", validators=[DataRequired()])
    repair_end_date = DateField("End date", validators=[DataRequired()])
    vendor_name = StringField("Vendor name", validators=[DataRequired()])
    nhtsa_recall_number = StringField("NHTSA recall number")
    total_cost = FloatField("Repair cost", validators=[DataRequired()])
    repair_description = StringField("Description", validators=[DataRequired()])

class ManufacturerForm(FlaskForm):
    manufacturer_name = StringField("Enter new manufacturer name", validators=[DataRequired()])

class VehicleTypeForm(FlaskForm):
    vehicle_type = StringField("Enter new vehicle type", validators=[DataRequired()])

class VendorSearchForm(FlaskForm):
    vendor_name = StringField("Search Vendor by name", validators=[DataRequired()])
