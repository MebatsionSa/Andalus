
from django.utils.safestring import mark_safe
from django.core.exceptions  import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.timezone import now

countries = (
    'Afghanistan', 'Albania', 'Algeria', 'American', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua', 'Argentina', 'Armenia', 'Aruba', 'Australia',
    'Austria', 'Azerbaijan', 'Bahamas,', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia', 'Botswana', 
    'Bouvet', 'Brazil', 'British', 'British', 'Brunei', 'Bulgaria', 'Burkina', 'Burma', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape', 'Cayman', 'Central', 'Chad', 
    'Chile', 'China', 'Christmas', 'Cocos', 'Colombia', 'Comoros', 'Congo,', 'Congo,', 'Cook', 'Costa', 'Cote', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech', 'Denmark', 
    'Djibouti', 'Dominica', 'Dominican', 'East', 'Ecuador', 'Egypt', 'El', 'Equatorial', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland', 'Faroe', 'Fiji', 'Finland', 'France', 
    'France,', 'French', 'French', 'French', 'Gabon', 'Gambia,', 'Gaza', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 
    'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard', 'Holy', 'Honduras', 'Hong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 
    'Ireland', 'Isle', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea,', 'Korea,', 'Kuwait', 'Kyrgyzstan', 'Laos', 
    'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 
    'Mali', 'Malta', 'Marshall', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia,', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 
    'Morocco', 'Mozambique', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New', 'New', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk', 'Northern', 'Norway', 'Oman', 
    'Pakistan', 'Palau', 'Panama', 'Papua', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda', 
    'Saint', 'Saint', 'Saint', 'Saint', 'Saint', 'Saint', 'Saint', 'Samoa', 'San', 'Sao', 'Saudi', 'Senegal', 'Serbia', 'Seychelles', 'Sierra', 'Singapore', 'Sint', 'Slovakia', 
    'Slovenia', 'Solomon', 'Somalia', 'South', 'South', 'South', 'Spain', 'Sri', 'Sudan', 'Suriname', 'Svalbard', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 
    'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tokelau', 'Tonga', 'Trinidad', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks', 'Tuvalu', 'Uganda', 'Ukraine', 'United', 
    'United', 'United', 'United', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Virgin', 'Wallis', 'West', 'Western', 'Yemen', 'Zambia', 'Zimbabwe'
    )


countries_dict = {
    'Afghanistan': 'AFG', 'Albania': 'ALB', 'Algeria': 'DZA', 'American': 'ASM', 'Andorra': 'AND', 'Angola': 'AGO', 'Anguilla': 'AIA', 'Antarctica': 'ATA',
    'Antigua': 'ATG', 'Argentina': 'ARG', 'Armenia': 'ARM', 'Aruba': 'ABW', 'Australia': 'AUS', 'Austria': 'AUT', 'Azerbaijan': 'AZE', 'Bahamas,': 'BHS', 'Bahrain': 'BHR', 
    'Bangladesh': 'BGD', 'Barbados': 'BRB', 'Belarus': 'BLR', 'Belgium': 'BEL', 'Belize': 'BLZ', 'Benin': 'BEN', 'Bermuda': 'BMU', 'Bhutan': 'BTN', 'Bolivia': 'BOL',
    'Bosnia': 'BIH', 'Botswana': 'BWA', 'Bouvet': 'BVT', 'Brazil': 'BRA', 'British': 'IOT', 'British': 'VGB', 'Brunei': 'BRN', 'Bulgaria': 'BGR', 'Burkina': 'BFA',
    'Burma': 'MMR', 'Burundi': 'BDI', 'Cambodia': 'KHM', 'Cameroon': 'CMR', 'Canada': 'CAN', 'Cape': 'CPV', 'Cayman': 'CYM', 'Central': 'CAF', 'Chad': 'TCD', 'Chile': 'CHL', 
    'China': 'CHN', 'Christmas': 'CXR', 'Cocos': 'CCK', 'Colombia': 'COL', 'Comoros': 'COM', 'Congo,': 'COD', 'Congo,': 'COG', 'Cook': 'COK', 'Costa': 'CRI', 'Cote': 'CIV', 
    'Croatia': 'HRV', 'Cuba': 'CUB', 'Curacao': 'CUW', 'Cyprus': 'CYP', 'Czech': 'CZE', 'Denmark': 'DNK', 'Djibouti': 'DJI', 'Dominica': 'DMA', 'Dominican': 'DOM', 
    'East': 'TLS', 'Ecuador': 'ECU', 'Egypt': 'EGY', 'El': 'SLV', 'Equatorial': 'GNQ', 'Eritrea': 'ERI', 'Estonia': 'EST', 'Ethiopia': 'ETH', 'Falkland': 'FLK', 
    'Faroe': 'FRO', 'Fiji': 'FJI', 'Finland': 'FIN', 'France': 'FRA', 'France,': 'FXX', 'French': 'GUF', 'French': 'PYF', 'French': 'ATF', 'Gabon': 'GAB', 'Gambia,': 'GMB', 
    'Gaza': 'PSE', 'Georgia': 'GEO', 'Germany': 'DEU', 'Ghana': 'GHA', 'Gibraltar': 'GIB', 'Greece': 'GRC', 'Greenland': 'GRL', 'Grenada': 'GRD', 'Guadeloupe': 'GLP', 
    'Guam': 'GUM', 'Guatemala': 'GTM', 'Guernsey': 'GGY', 'Guinea': 'GIN', 'Guinea-Bissau': 'GNB', 'Guyana': 'GUY', 'Haiti': 'HTI', 'Heard': 'HMD', 'Holy': 'VAT', 
    'Honduras': 'HND', 'Hong': 'HKG', 'Hungary': 'HUN', 'Iceland': 'ISL', 'India': 'IND', 'Indonesia': 'IDN', 'Iran': 'IRN', 'Iraq': 'IRQ', 'Ireland': 'IRL', 'Isle': 'IMN', 
    'Israel': 'ISR', 'Italy': 'ITA', 'Jamaica': 'JAM', 'Japan': 'JPN', 'Jersey': 'JEY', 'Jordan': 'JOR', 'Kazakhstan': 'KAZ', 'Kenya': 'KEN', 'Kiribati': 'KIR', 
    'Korea,': 'PRK', 'Korea,': 'KOR', 'Kuwait': 'KWT', 'Kyrgyzstan': 'KGZ', 'Laos': 'LAO', 'Latvia': 'LVA', 'Lebanon': 'LBN', 'Lesotho': 'LSO', 'Liberia': 'LBR', 
    'Libya': 'LBY', 'Liechtenstein': 'LIE', 'Lithuania': 'LTU', 'Luxembourg': 'LUX', 'Macau': 'MAC', 'Macedonia': 'MKD', 'Madagascar': 'MDG', 'Malawi': 'MWI', 
    'Malaysia': 'MYS', 'Maldives': 'MDV', 'Mali': 'MLI', 'Malta': 'MLT', 'Marshall': 'MHL', 'Martinique': 'MTQ', 'Mauritania': 'MRT', 'Mauritius': 'MUS', 'Mayotte': 'MYT', 
    'Mexico': 'MEX', 'Micronesia,': 'FSM', 'Moldova': 'MDA', 'Monaco': 'MCO', 'Mongolia': 'MNG', 'Montenegro': 'MNE', 'Montserrat': 'MSR', 'Morocco': 'MAR', 
    'Mozambique': 'MOZ', 'Namibia': 'NAM', 'Nauru': 'NRU', 'Nepal': 'NPL', 'Netherlands': 'NLD', 'New': 'NCL', 'New': 'NZL', 'Nicaragua': 'NIC', 'Niger': 'NER', 
    'Nigeria': 'NGA', 'Niue': 'NIU', 'Norfolk': 'NFK', 'Northern': 'MNP', 'Norway': 'NOR', 'Oman': 'OMN', 'Pakistan': 'PAK', 'Palau': 'PLW', 'Panama': 'PAN', 'Papua': 'PNG', 
    'Paraguay': 'PRY', 'Peru': 'PER', 'Philippines': 'PHL', 'Pitcairn': 'PCN', 'Poland': 'POL', 'Portugal': 'PRT', 'Puerto': 'PRI', 'Qatar': 'QAT', 'Reunion': 'REU', 
    'Romania': 'ROU', 'Russia': 'RUS', 'Rwanda': 'RWA', 'Saint': 'BLM', 'Saint': 'SHN', 'Saint': 'KNA', 'Saint': 'LCA', 'Saint': 'MAF', 'Saint': 'SPM', 'Saint': 'VCT', 
    'Samoa': 'WSM', 'San': 'SMR', 'Sao': 'STP', 'Saudi': 'SAU', 'Senegal': 'SEN', 'Serbia': 'SRB', 'Seychelles': 'SYC', 'Sierra': 'SLE', 'Singapore': 'SGP', 'Sint': 'SXM', 
    'Slovakia': 'SVK', 'Slovenia': 'SVN', 'Solomon': 'SLB', 'Somalia': 'SOM', 'South': 'ZAF', 'South': 'SGS', 'South': 'SSD', 'Spain': 'ESP', 'Sri': 'LKA', 'Sudan': 'SDN', 
    'Suriname': 'SUR', 'Svalbard': 'SJM', 'Swaziland': 'SWZ', 'Sweden': 'SWE', 'Switzerland': 'CHE', 'Syria': 'SYR', 'Taiwan': 'TWN', 'Tajikistan': 'TJK', 'Tanzania': 'TZA', 
    'Thailand': 'THA', 'Togo': 'TGO', 'Tokelau': 'TKL', 'Tonga': 'TON', 'Trinidad': 'TTO', 'Tunisia': 'TUN', 'Turkey': 'TUR', 'Turkmenistan': 'TKM', 'Turks': 'TCA', 
    'Tuvalu': 'TUV', 'Uganda': 'UGA', 'Ukraine': 'UKR', 'United': 'ARE', 'United': 'GBR', 'United': 'USA', 'United': 'UMI', 'Uruguay': 'URY', 'Uzbekistan': 'UZB', 
    'Vanuatu': 'VUT', 'Venezuela': 'VEN', 'Vietnam': 'VNM', 'Virgin': 'VIR', 'Wallis': 'WLF', 'West': 'PSE', 'Western': 'ESH', 'Yemen': 'YEM', 'Zambia': 'ZMB', 
    'Zimbabwe': 'ZWE'
    }
choice = ((i, i) for i in countries)

class Role(models.Model):
    role = models.CharField(max_length=200)
    short_name = models.CharField(max_length=10)
    def __str__(self):
        return self.short_name


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category


class Campus(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='', blank=True)
    country = models.CharField(max_length=200, choices=choice, default="Ethiopia")

    def __str__(self):
        return self.short_name

    class Meta:
        unique_together = ('name', 'country')

    def logo_tag(self):
        return mark_safe('<img src="%s" width="150" height="150"/>' % self.logo.url)

    logo_tag.short_description = 'Logo'
    logo_tag.allow_tags = True

    def flag(self):
        return countries_dict[self.country]
    

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password='admin', role=None, category=None):
        """
        Creates and saves a User with the given email 
        and <li ><a href="#">{{user.username}}</a></li>password.
        """
        if not username:
            raise ValueError('Users must have an user name')
        
        if not first_name:
            raise ValueError('Users must have an first name')

        if not last_name:
            raise ValueError('Users must have an last name')

        if not email:
            raise ValueError('Users must have an email address')

        if not role:
            raise ValueError('Users must have at least 1 role')
    
        if not category:
            raise ValueError('Users must have a category')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            category=category,
            register_date=timezone.now().date(),
        )
        user.set_password(password)
        user.save(using=self._db)
        user.role.set([role])
        return user

    def create_superuser(self,username, email, password):
        """
        Creates and saves a superuser with the given email, password ...
        """
        role = Role.objects.get(short_name='admin')
        category = Category.objects.get(category='System')
        user = self.create_user(
            username=username,
            first_name=' ',
            last_name=' ',
            email=email,
            password=password,
            role=role,
            category=category,
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 09******** or +2519******** up to 15 digits allowed',
        )
        
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    sex = models.CharField(max_length=200, choices=(('male', 'male'), ('female', 'female')))
    photo = models.ImageField(blank=True, upload_to='', default='null.png')
    score = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, default=1)
    register_date = models.DateField(default = now)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150"/>' % self.photo.url)

    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True

    def __str__(self):
        # return self.username
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Team(models.Model):

    username = models.CharField(max_length=200, unique=True)
    member = models.ManyToManyField(User,   limit_choices_to={'category__category': 'Participant', 'role__role': 'Team Member'})
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, default=1)
    score = models.IntegerField(default=0)
    register_date = models.DateField()
 
    # def clean(self, *args, **kwargs):
    #     if self.member.count() > 3:
    #         raise ValidationError("Maximum number of user in 1 team is 3.")
    #     super(Team, self).clean(*args, **kwargs)

    def __str__(self):
        return self.username


class ActiveTeam(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'category__category': 'Participant', 'role__role': 'Team Member'})
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.team:
            return self.user.username + ' from team ' + self.team.username
        else:
            return self.user.username + ' from empty team'