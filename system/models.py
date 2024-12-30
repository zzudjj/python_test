from django.db import models


# Create your models here.


class Passenger(models.Model):
    """乘客表"""
    sex_choices = (('男', '男'), ('女', '女'))
    telephone = models.CharField(max_length=11, primary_key=True, verbose_name='电话号码')
    name = models.CharField(max_length=20, verbose_name='姓名')
    password = models.CharField(max_length=32, verbose_name='密码')
    sex = models.CharField(max_length=3, verbose_name='性别', choices=sex_choices)

    class Meta:
        db_table = 'passenger'
        constraints = [
            models.CheckConstraint(check=models.Q(sex='男') | models.Q(sex='女'), name='passenger_check_sex_value')
        ]


class Driver(models.Model):
    """司机表"""
    sex_choices = (('男', '男'), ('女', '女'))
    id = models.CharField(max_length=6, verbose_name='司机工号', primary_key=True)
    name = models.CharField(max_length=20, verbose_name='姓名')
    password = models.CharField(max_length=32, verbose_name='密码')
    sex = models.CharField(max_length=3, verbose_name='性别', choices=sex_choices)

    class Meta:
        db_table = 'driver'
        constraints = [
            models.CheckConstraint(check=models.Q(sex='男') | models.Q(sex='女'), name='driver_check_sex_value')
        ]

    def __str__(self):
        return self.id


class Manager(models.Model):
    """公司管理人员表"""
    sex_choices = (('男', '男'), ('女', '女'))
    id = models.CharField(max_length=6, verbose_name='管理员工号', primary_key=True)
    name = models.CharField(max_length=20, verbose_name='姓名')
    password = models.CharField(max_length=32, verbose_name='密码')
    sex = models.CharField(max_length=3, verbose_name='性别', choices=sex_choices)

    class Meta:
        db_table = 'manager'
        constraints = [
            models.CheckConstraint(check=models.Q(sex='男') | models.Q(sex='女'), name='manager_check_sex_value')
        ]


class DriverTelephone(models.Model):
    """司机电话表"""
    telephone = models.CharField(max_length=11, primary_key=True, verbose_name='电话号码')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='司机工号')

    class Meta:
        db_table = 'driver_telephone'


class ManagerTelephone(models.Model):
    """公司管理人员电话表"""
    telephone = models.CharField(max_length=11, primary_key=True, verbose_name='电话号码')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name='管理人员工号')

    class Meta:
        db_table = 'manager_telephone'


class Line(models.Model):
    """线路表"""
    id = models.IntegerField(primary_key=True, verbose_name='线路编号')

    class Meta:
        db_table = 'line'

    def __str__(self):
        return str(self.id)


class Bus(models.Model):
    """公共汽车表"""
    plate_number = models.CharField(max_length=10, primary_key=True, verbose_name='车牌号')
    passenger_capacity = models.IntegerField(verbose_name='载客量')
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, verbose_name='所属线路')

    class Meta:
        db_table = 'bus'

    def __str__(self):
        return self.plate_number


class Site(models.Model):
    """站点表"""
    id = models.AutoField(primary_key=True, verbose_name='站点编号')
    name = models.CharField(max_length=20, unique=True, verbose_name='站点名称')

    class Meta:
        db_table = 'site'


class Violation(models.Model):
    """违章表"""
    choices = ((0, '未处理'), (1, '已通过'), (2, '未通过'))
    id = models.AutoField(primary_key=True, verbose_name='违章编号')
    title = models.CharField(max_length=90, verbose_name='违章标题')
    text = models.TextField(verbose_name="违章内容")
    status = models.IntegerField(choices=choices, default=0, verbose_name="处理状态")
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, verbose_name="处理人员")
    passenger_tel = models.ForeignKey(Passenger, on_delete=models.CASCADE, verbose_name='投诉人电话')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='被投诉司机工号')

    class Meta:
        db_table = 'violation'


class Announcement(models.Model):
    """公告表"""
    id = models.AutoField(primary_key=True, verbose_name='公告编号')
    title = models.CharField(max_length=90, verbose_name='公告标题')
    text = models.TextField(verbose_name="公告内容")
    date = models.DateField(verbose_name='发布日期')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name="发布者")

    class Meta:
        db_table = 'announcement'


class Contain(models.Model):
    """包含关系表"""
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='站点编号', related_name='site')
    line = models.ForeignKey(Line, on_delete=models.CASCADE, verbose_name='线路编号')
    last_site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, verbose_name='上一站点编号', related_name='last_site')
    next_site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, verbose_name='下一站点编号', related_name='next_site')

    class Meta:
        db_table = 'contain'
        unique_together = (('site', 'line'),)


class Ride(models.Model):
    """乘坐关系表"""
    id = models.AutoField(primary_key=True)
    plate_number = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name='车牌号')
    passenger_tel = models.ForeignKey(Passenger, on_delete=models.CASCADE, verbose_name='电话号码')
    travel_time = models.DateTimeField(verbose_name='乘坐时间')

    class Meta:
        db_table = 'ride'
        unique_together = (('plate_number', 'passenger_tel','travel_time'),)


class Drive(models.Model):
    """驾驶关系表"""
    id = models.AutoField(primary_key=True)
    plate_number = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name='车牌号')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='司机工号')
    start_time = models.DateTimeField(verbose_name='值班开始时间')
    end_time = models.DateTimeField(verbose_name='值班结束时间')

    class Meta:
        db_table = 'drive'
        unique_together = (('plate_number', 'start_time'),)


# class Complaint(models.Model):
#     """投诉关系表"""
#     id = models.AutoField(primary_key=True)
#     violation = models.ForeignKey(Violation, on_delete=models.CASCADE, verbose_name='违章编号')
#     passenger_tel = models.ForeignKey(Passenger, on_delete=models.CASCADE, verbose_name='投诉人电话')
#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='被投诉司机工号')
#
#     class Meta:
#         db_table = 'complaint'
#         unique_together = (('driver', 'passenger_tel', 'violation'),)


class LineView(models.Model):
    """线路站点视图"""
    id = models.IntegerField(primary_key=True)
    site_id = models.IntegerField()
    line_id = models.IntegerField()
    last_site_id = models.IntegerField()
    next_site_id = models.IntegerField()
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'line_view'


class DriverView(models.Model):
    """司机信息视图"""
    id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=3)
    telephone = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'driver_view'


class WorkView(models.Model):
    """值班信息视图"""
    id = models.IntegerField(primary_key=True)
    driver_id = models.CharField(max_length=6)
    name = models.CharField(max_length=20)
    plate_number_id = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'work_view'


class RideView(models.Model):
    """乘车记录视图"""
    id = models.IntegerField(primary_key=True)
    plate_number = models.CharField(max_length=10)
    line_id = models.IntegerField()
    passenger_tel_id = models.CharField(max_length=11)
    travel_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ride_view'


class ViolationView(models.Model):
    """违章信息视图"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=90)
    text = models.TextField()
    status = models.IntegerField()
    manager_id = models.CharField(max_length=6)
    passenger_tel_id = models.CharField(max_length=11)
    driver_id = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'violation_view'


class AnnouncementView(models.Model):
    """公告信息视图"""
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=90)
    text = models.TextField()
    date = models.DateField()
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'announcement_view'

