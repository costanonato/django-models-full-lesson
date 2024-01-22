import uuid

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=250)


class EmployeeStatus(models.TextChoices):
    ACTIVE = "act"
    INACTIVE = "inact"


class Employee(BaseModel):
    name = models.CharField(max_length=250)
    status = models.CharField(
        max_length=20,
        choices=EmployeeStatus.choices,
        default=EmployeeStatus.ACTIVE,
    )
    departments = models.ManyToManyField(Department, through="Assignment")
    profile = models.OneToOneField("Profile", on_delete=models.CASCADE, null=True)

    def deactivate(self):
        self.status = EmployeeStatus.INACTIVE
        self.save()

    def activate(self):
        self.status = EmployeeStatus.ACTIVE
        self.save()

    @property
    def basic_info(self):
        return f"{self.name} - {self.status}"

    def save(self, *args, **kwargs):
        if self.name == "John Doe":
            self.status = EmployeeStatus.INACTIVE

        super().save(*args, **kwargs)

    def __str__(self):
        return self.basic_info


class Assignment(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    joined_at = models.DateTimeField()
    left_at = models.DateTimeField(null=True)


class Profile(BaseModel):
    date_of_birth = models.DateField()
    address = models.TextField()
