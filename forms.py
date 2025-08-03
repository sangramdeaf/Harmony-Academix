from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username / वापरकर्ता नाव', validators=[DataRequired()])
    password = PasswordField('Password / पासवर्ड', validators=[DataRequired()])
    submit = SubmitField('Login / प्रवेश')

class RegistrationForm(FlaskForm):
    username = StringField('Username / वापरकर्ता नाव', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email / ईमेल', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name / पूर्ण नाव', validators=[DataRequired()])
    password = PasswordField('Password / पासवर्ड', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password / पासवर्ड पुष्टी', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register / नोंदणी')

class AdmissionFormForm(FlaskForm):
    # School Information
    school_name = StringField('शाळेचे नाव', validators=[DataRequired()])
    continuous_student_id = StringField('विद्यार्थी सतत ID')
    udise_pen = StringField('U-DISE+ पोर्टल SDMS - STUDENT PEN')
    admission_class = StringField('प्रवेश इयत्ता')
    
    # Personal Information
    birth_register_no = StringField('जन्माचा रजिस्टर नं.')
    aadhaar_no = StringField('आधार कार्ड नं.')
    birth_date = DateField('जन्मतारीख')
    admission_date = DateField('शाळेत प्रवेश तारीख')
    gender = SelectField('लिंग', choices=[('', 'निवडा'), ('male', 'मुलगा'), ('female', 'मुलगी')])
    
    # Photos
    student_photo = FileField('विद्यार्थ्याचे फोटो', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    parent_photo = FileField('पालकांचे फोटो', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    
    # Names
    first_name_marathi = StringField('प्रथम नाव (मराठी)', validators=[DataRequired()])
    last_name_marathi = StringField('आडनाव (मराठी)', validators=[DataRequired()])
    father_name = StringField('वडिलांचे नाव', validators=[DataRequired()])
    mother_name = StringField('आईचे नाव', validators=[DataRequired()])
    birth_date_words = StringField('जन्मतारीख अक्षरी')
    
    # Additional Information
    religion = StringField('धर्म')
    caste = StringField('जात')
    sub_caste = StringField('पोटजात')
    caste_certificate = StringField('जात प्रमाण')
    is_minority = BooleanField('अल्पसंख्याक')
    nationality = StringField('राष्ट्रत्व')
    mother_tongue = StringField('मातृभाषा')
    mobile_number = StringField('मोबाईल क्रमांक')
    
    # BPL and Disability
    bpl_status = BooleanField('BPL स्थिती')
    bpl_number = StringField('BPL क्रमांक')
    disability_status = BooleanField('दिव्यांग स्थिती')
    disability_type = StringField('दिव्यांग प्रकार')
    
    # Parent and Address
    parent_full_name = StringField('पालकांचे संपूर्ण नाव', validators=[DataRequired()])
    address = TextAreaField('पत्ता', validators=[DataRequired()])
    
    submit = SubmitField('जमा करा')

class BonafideFormForm(FlaskForm):
    student_name = StringField('विद्यार्थ्याचे पूर्ण नाव', validators=[DataRequired()])
    academic_year = StringField('शैक्षणिक वर्ष', validators=[DataRequired()])
    class_standard = StringField('इयत्ता', validators=[DataRequired()])
    division = StringField('तुकडी', validators=[DataRequired()])
    conduct = StringField('वर्तन', validators=[DataRequired()])
    caste = StringField('जात', validators=[DataRequired()])
    birth_date = DateField('जन्मतारीख', validators=[DataRequired()])
    birth_place = StringField('जन्मस्थान', validators=[DataRequired()])
    school_place = StringField('शाळेचे स्थळ', validators=[DataRequired()])
    submit = SubmitField('दाखला तयार करा')

class PratinidhanFormForm(FlaskForm):
    student_name = StringField('विद्यार्थ्याचे पूर्ण नाव / Student Name', validators=[DataRequired()])
    academic_year = StringField('शैक्षणिक वर्ष / Academic Year', validators=[DataRequired()])
    class_standard = StringField('इयत्ता / Class', validators=[DataRequired()])
    division = StringField('तुकडी / Division', validators=[DataRequired()])
    conduct = StringField('वर्तन / Conduct', validators=[DataRequired()])
    caste = StringField('जात / Caste', validators=[DataRequired()])
    birth_date = DateField('जन्मतारीख / Date of Birth', validators=[DataRequired()])
    birth_place = StringField('जन्मस्थान / Place of Birth', validators=[DataRequired()])
    school_place = StringField('शाळेचे स्थळ / School Location', validators=[DataRequired()])
    submit = SubmitField('प्रमाणपत्र तयार करा / Generate Certificate')

class ProfileForm(FlaskForm):
    full_name = StringField('पूर्ण नाव / Full Name', validators=[Optional()])
    email = StringField('ईमेल / Email', validators=[Optional(), Email()])
    phone_number = StringField('फोन नंबर / Phone Number', validators=[Optional()])
    address = TextAreaField('पत्ता / Address', validators=[Optional()])
    date_of_birth = DateField('जन्मतारीख / Date of Birth', validators=[Optional()])
    profile_photo = FileField('प्रोफाइल फोटो / Profile Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('प्रोफाइल अपडेट करा / Update Profile')

class ChatForm(FlaskForm):
    api_key = StringField('Hugging Face API Key', validators=[DataRequired()], render_kw={'placeholder': 'Enter your Hugging Face API key'})
    message = TextAreaField('संदेश / Message', validators=[DataRequired()], render_kw={'placeholder': 'आपला प्रश्न येथे लिहा / Type your question here'})
    submit = SubmitField('पाठवा / Send')
