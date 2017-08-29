from django.db import models
from datetime import datetime

ZOOM_CHOICES = (
        ('region', 'region'), ('country', 'country'), ('county', 'county'),
        ('edist', 'edist'), ('area', 'area'))

# Create your models here.
class Sale(models.Model):
    uid = models.IntegerField()
    sale_date = models.DateField()

    address = models.CharField(max_length=500)
    postcode = models.CharField(max_length=50)

    COUNTY_CHOICES = (
        ('Galway','Galway'), ('Leitrim','Leitrim'), ('Mayo','Mayo'),
        ('Roscommon','Roscommon'), ('Sligo','Sligo'), ('Carlow','Carlow'),
        ('Dublin','Dublin'), ('Kildare','Kildare'), ('Kilkenny','Kilkenny'),
        ('Laois','Laois'), ('Longford','Longford'), ('Louth','Louth'),
        ('Meath','Meath'), ('Offaly','Offaly'), ('Westmeath','Westmeath'),
        ('Wexford','Wexford'), ('Wicklow','Wicklow'), ('Clare','Clare'),
        ('Cork','Cork'), ('Kerry','Kerry'), ('Limerick','Limerick'),
        ('Tipperary','Tipperary'), ('Waterford','Waterford'),
        ('Cavan','Cavan'), ('Donegal','Donegal'), ('Monaghan','Monaghan')
    )

    county = models.CharField(max_length=9, choices=COUNTY_CHOICES,
                              default='Dublin')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    nfma = models.CharField(max_length=3, choices=(('yes', 'yes'),
                            ('no', 'no')), default='no')
    vat_ex = models.CharField(max_length=3, choices=(('yes', 'yes'),
                            ('no', 'no')), default='no')
    DoP_CHOICES = (
        ('Second-Hand Dwelling house /Apartment','Second-Hand'),
        ('New Dwelling house /Apartment','New')
    )

    DoP = models.CharField(max_length=40, choices=DoP_CHOICES,
                              default='Second-Hand Dwelling house /Apartment')

    PSD_CHOICES = (
        ('greater than or equal to 38 sq metres and less than 125 sq '
         'metres', 'GT38 LS125'),
        ('greater than 125 sq metres','GT125'),
        ('less than 38 sq metres', 'LT38'),('Unknown', 'Unknown')
    )

    PSD = models.CharField(max_length=70, choices=DoP_CHOICES,
                           default='Unknown')

    REGION_CHOICES = (
        ('Connacht','Connacht'), ('Leinster', 'Leinster'),
        ('Munster', 'Munster'), ('Ulster', 'Ulster'))

    region = models.CharField(max_length=8,choices=REGION_CHOICES,
                              default='Leinster')
    latitude = models.DecimalField(max_digits=9,decimal_places=7)
    longitude =  models.DecimalField(max_digits=10,decimal_places=7)

    ed = models.CharField(max_length=100)

    quality = models.CharField(max_length=4)

    def __str__(self):
        return str(self.id)


class CSORef(models.Model):
    uid = models.CharField(max_length=10)

    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')

    desc = models.CharField(max_length=100)


class SexAgeMarriage(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    age_04 = models.IntegerField()
    age_59 = models.IntegerField()
    age_1014 = models.IntegerField()
    age_1519 = models.IntegerField()
    age_2024 = models.IntegerField()
    age_2529 = models.IntegerField()
    age_3034 = models.IntegerField()
    age_3539 = models.IntegerField()
    age_4044 = models.IntegerField()
    age_4549 = models.IntegerField()
    age_5054 = models.IntegerField()
    age_5559 = models.IntegerField()
    age_6064 = models.IntegerField()
    age_6569 = models.IntegerField()
    age_7074 = models.IntegerField()
    age_7579 = models.IntegerField()
    age_8084 = models.IntegerField()
    age_85p = models.IntegerField()
    pop = models.IntegerField()
    single = models.IntegerField()
    married = models.IntegerField()
    separated = models.IntegerField()
    divorced = models.IntegerField()
    widowed = models.IntegerField()
    mar_total = models.IntegerField()

    def __str__(self):
        return str(self.id)


class PoBNat(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    pob_ire = models.IntegerField()
    pob_uk = models.IntegerField()
    pob_pol = models.IntegerField()
    pob_lit = models.IntegerField()
    pob_oeu = models.IntegerField()
    pob_row = models.IntegerField()
    pob_ns = models.IntegerField()
    pob_tot = models.IntegerField()

    nat_ire = models.IntegerField()
    nat_uk = models.IntegerField()
    nat_pol = models.IntegerField()
    nat_lit = models.IntegerField()
    nat_oeu = models.IntegerField()
    nat_row = models.IntegerField()
    nat_ns = models.IntegerField()
    nat_tot = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Families(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    child_0 = models.IntegerField()
    child_1 = models.IntegerField()
    child_2 = models.IntegerField()
    child_3 = models.IntegerField()
    child_4 = models.IntegerField()
    child_ge5 = models.IntegerField()

    pre_fam = models.IntegerField()
    empty_nest = models.IntegerField()
    retired = models.IntegerField()
    pre_s = models.IntegerField()
    early_s = models.IntegerField()
    pre_adol = models.IntegerField()
    adol = models.IntegerField()
    adult = models.IntegerField()
    fam_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class PrivHH(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    one_p = models.IntegerField()
    married = models.IntegerField()
    cohab_couple = models.IntegerField()
    married_kids = models.IntegerField()
    cohab_couple_kids = models.IntegerField()
    father_kids = models.IntegerField()
    mother_kids = models.IntegerField()
    couple_others = models.IntegerField()
    couple_kids_others = models.IntegerField()
    father_kids_others = models.IntegerField()
    mother_kids_others = models.IntegerField()
    two_or_more_fu = models.IntegerField()
    non_fam_hh = models.IntegerField()
    two_or_more_nrp = models.IntegerField()
    hstat_total = models.IntegerField()

    one_phh = models.IntegerField()
    two_phh = models.IntegerField()
    three_phh = models.IntegerField()
    four_phh = models.IntegerField()
    five_phh = models.IntegerField()
    six_phh = models.IntegerField()
    seven_phh = models.IntegerField()
    ge_eight_phh = models.IntegerField()
    phh_total_hh = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Housing(models.Model):
    uid = models.CharField(max_length=100)
    zoom = models.CharField(max_length=70, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    house_bung = models.IntegerField()
    apart = models.IntegerField()
    bedsit = models.IntegerField()
    caravan = models.IntegerField()
    type_ns = models.IntegerField()
    type_total_hh = models.IntegerField()

    l1919 = models.IntegerField()
    b19_45 = models.IntegerField()
    b46_60 = models.IntegerField()
    b61_70 = models.IntegerField()
    b71_80 = models.IntegerField()
    b81_90 = models.IntegerField()
    b91_00 = models.IntegerField()
    b01_10 = models.IntegerField()
    g11 = models.IntegerField()
    h_age_ns = models.IntegerField()
    h_age_total_hh = models.IntegerField()

    oo_wm = models.IntegerField()
    oo_wom = models.IntegerField()
    rent_pl = models.IntegerField()
    rent_la = models.IntegerField()
    rent_vol = models.IntegerField()
    rent_free = models.IntegerField()
    occu_ns = models.IntegerField()
    occu_total_hh = models.IntegerField()

    rooms_1 = models.IntegerField()
    rooms_2 = models.IntegerField()
    rooms_3 = models.IntegerField()
    rooms_4 = models.IntegerField()
    rooms_5 = models.IntegerField()
    rooms_6 = models.IntegerField()
    rooms_7 = models.IntegerField()
    rooms_ge8 = models.IntegerField()
    rooms_ns = models.IntegerField()
    rooms_total_hh = models.IntegerField()

    occupied = models.IntegerField()
    temp_unoc = models.IntegerField()
    unoc_hol = models.IntegerField()
    unoccupied = models.IntegerField()

    def __str__(self):
        return str(self.id)

class PrincStat(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    work = models.IntegerField()
    lffj = models.IntegerField()
    unemployed = models.IntegerField()
    student = models.IntegerField()
    home_fam = models.IntegerField()
    retired = models.IntegerField()
    sick_dis = models.IntegerField()
    stat_other = models.IntegerField()
    stat_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class SocClass(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    prof_worker = models.IntegerField()
    manage_tech = models.IntegerField()
    non_manual = models.IntegerField()
    skilled_manual = models.IntegerField()
    semi_skilled = models.IntegerField()
    unskilled = models.IntegerField()
    class_other = models.IntegerField()
    class_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Education(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES, default='country')
    year = models.IntegerField()

    nfe = models.IntegerField()
    primary = models.IntegerField()
    l_secondary = models.IntegerField()
    u_secondary = models.IntegerField()
    tech_vocat = models.IntegerField()
    apprentice = models.IntegerField()
    high_cert = models.IntegerField()
    bach = models.IntegerField()
    bach_hons = models.IntegerField()
    postgrad = models.IntegerField()
    doctorate = models.IntegerField()
    ed_ns = models.IntegerField()
    ed_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Commuting(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    foot = models.IntegerField()
    bike = models.IntegerField()
    bus = models.IntegerField()
    train = models.IntegerField()
    mbike = models.IntegerField()
    car_d = models.IntegerField()
    car_p = models.IntegerField()
    van = models.IntegerField()
    other = models.IntegerField()
    method_ns = models.IntegerField()
    method_total = models.IntegerField()

    u15m = models.IntegerField()
    b15_30m = models.IntegerField()
    b30_45m = models.IntegerField()
    b45_60m = models.IntegerField()
    b60_90m = models.IntegerField()
    o90m = models.IntegerField()
    time_ns = models.IntegerField()
    time_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Occupation(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    man_dir_sos = models.IntegerField()
    prof_oc = models.IntegerField()
    assoc_prof_tech = models.IntegerField()
    admin_sec = models.IntegerField()
    skilled_trade = models.IntegerField()
    caring_leisure = models.IntegerField()
    sales_cs = models.IntegerField()
    process_plant = models.IntegerField()
    elementary = models.IntegerField()
    occ_ns = models.IntegerField()
    occ_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Industries(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    ag_for_fish = models.IntegerField()
    build_construct = models.IntegerField()
    manufac = models.IntegerField()
    comm_trade = models.IntegerField()
    trans_coms = models.IntegerField()
    pub_admin = models.IntegerField()
    prof_ser = models.IntegerField()
    ind_other = models.IntegerField()
    ind_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class AgeExt(models.Model):
    uid = models.CharField(max_length=10)
    zoom = models.CharField(max_length=7, choices=ZOOM_CHOICES,
                            default='country')
    year = models.IntegerField()

    age_04_m = models.IntegerField()
    age_59_m = models.IntegerField()
    age_1014_m = models.IntegerField()
    age_1519_m = models.IntegerField()
    age_2024_m = models.IntegerField()
    age_2529_m = models.IntegerField()
    age_3034_m = models.IntegerField()
    age_3539_m = models.IntegerField()
    age_4044_m = models.IntegerField()
    age_4549_m = models.IntegerField()
    age_5054_m = models.IntegerField()
    age_5559_m = models.IntegerField()
    age_6064_m = models.IntegerField()
    age_6569_m = models.IntegerField()
    age_7074_m = models.IntegerField()
    age_7579_m = models.IntegerField()
    age_8084_m = models.IntegerField()
    age_85p_m = models.IntegerField()

    age_04_f = models.IntegerField()
    age_59_f = models.IntegerField()
    age_1014_f = models.IntegerField()
    age_1519_f = models.IntegerField()
    age_2024_f = models.IntegerField()
    age_2529_f = models.IntegerField()
    age_3034_f = models.IntegerField()
    age_3539_f = models.IntegerField()
    age_4044_f = models.IntegerField()
    age_4549_f = models.IntegerField()
    age_5054_f = models.IntegerField()
    age_5559_f = models.IntegerField()
    age_6064_f = models.IntegerField()
    age_6569_f = models.IntegerField()
    age_7074_f = models.IntegerField()
    age_7579_f = models.IntegerField()
    age_8084_f = models.IntegerField()
    age_85p_f = models.IntegerField()

    age_0 = models.IntegerField()
    age_1 = models.IntegerField()
    age_2 = models.IntegerField()
    age_3 = models.IntegerField()
    age_4 = models.IntegerField()
    age_5 = models.IntegerField()
    age_6 = models.IntegerField()
    age_7 = models.IntegerField()
    age_8 = models.IntegerField()
    age_9 = models.IntegerField()
    age_10 = models.IntegerField()
    age_11 = models.IntegerField()
    age_12 = models.IntegerField()
    age_13 = models.IntegerField()
    age_14 = models.IntegerField()
    age_15 = models.IntegerField()
    age_16 = models.IntegerField()
    age_17 = models.IntegerField()
    age_18 = models.IntegerField()
    age_19 = models.IntegerField()

    def __str__(self):
        return str(self.id)

class ReportedErrors(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    marker_uid = models.IntegerField()
    address_error = models.BooleanField()
    location_error = models.BooleanField()
    date_error = models.BooleanField()
    price_error = models.BooleanField()

    other_info = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)