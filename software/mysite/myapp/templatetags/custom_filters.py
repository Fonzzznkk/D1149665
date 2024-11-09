# custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(container, key):
    try:
        if isinstance(container, dict):
            return container.get(key, [])
        elif isinstance(container, list):
            # 將 key 轉換為整數索引來訪問列表中的項目
            index = int(key) - 1  # 將節次轉為 0 基數的索引
            return container[index] if 0 <= index < len(container) else None
    except (ValueError, IndexError, TypeError):
        return None
