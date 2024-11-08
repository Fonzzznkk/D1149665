from django.db import models

# 學生資料
class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)  # 學號，設為唯一值
    password = models.CharField(max_length=50)  # 密碼
    name = models.CharField(max_length=100)     # 姓名

    def __str__(self):
        return self.name
    
#所有課程資料
class Course(models.Model):
    # 定義欄位
    name = models.CharField(max_length=100, verbose_name="課程名稱")
    department = models.CharField(max_length=100, verbose_name="開課系所")
    time = models.CharField(max_length=50, verbose_name="上課時間")
    teacher = models.CharField(max_length=100, verbose_name="授課教師")
    language = models.CharField(max_length=50, verbose_name="授課語言")
    type = models.CharField(max_length=50, verbose_name="課程類型")
    information = models.CharField(max_length=5000, verbose_name="課程資訊")

    def __str__(self):
        return f"{self.name} - {self.department}"

    class Meta:
        verbose_name = "課程"
        verbose_name_plural = "課程"


#課表資料
class Curriculum(models.Model):
    # student_id 外鍵，指向 Student 模型
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="學生")
    
    # course_id 外鍵，指向 Course 模型
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name="課程")

    class Meta:
        verbose_name = "課表"
        verbose_name_plural = "課表"
        unique_together = ('student_id', 'course_id')  # 確保同一學生不會重複選修同一課程

    def __str__(self):
        return f"{self.student_id} - {self.course_id}"
