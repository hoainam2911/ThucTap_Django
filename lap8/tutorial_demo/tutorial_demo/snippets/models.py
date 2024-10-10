from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        Sử dụng Pygments để tạo nội dung HTML tô màu cho đoạn mã và lưu vào trường 'highlighted'.
        """
        # Lấy lexer dựa trên ngôn ngữ của đoạn mã
        lexer = get_lexer_by_name(self.language)
        
        # Xác định việc hiển thị số dòng
        linenos = 'table' if self.linenos else False
        
        # Thêm tiêu đề nếu có
        options = {'title': self.title} if self.title else {}
        
        # Tạo formatter để tô màu đoạn mã
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        
        # Tô màu đoạn mã và lưu vào trường 'highlighted'
        self.highlighted = highlight(self.code, lexer, formatter)
        
        # Gọi phương thức `save` của lớp cha để lưu đối tượng vào cơ sở dữ liệu
        super().save(*args, **kwargs)
