"""
    Copyright © 2018 PuroxyIO. All rights reserved.
    @author: Matt Massoodi
    @email: matt@puroxy.io
    @github: ex8
"""
from django.db import models

# Product types
PRODUCT_TYPES = (
    ('web', 'Web Hosting'),
    ('linux_vps', 'Linux VPS'),
    ('window_vps', 'Windows VPS'),
    ('onshore_dedicated', 'Onshore Dedicated'),
    ('offshore_dedicated', 'Offshore Dedicated'),
)
# Product status types
STATUS_TYPES = (
    ('complete', 'Complete'),
    ('in_progress', 'In Progress'),
    ('pending', 'Pending'),
    ('cancelled', 'Cancelled')
)
# Configuration form types, can add your own if need be
# If you do, you must implement it in product/forms.py
FORM_TYPES = (
    ('dropdown', 'Dropdown'),
    ('input', 'Input'),
)


class Product(models.Model):
    """
    Purpose: Product Model used to document different products
    @name: product name
    @slug: product slug URL (pre-populated from @name)
    @type: product type from list of choices
    @description: product description
    @price: product price
    @available: is product available ?
    @whm_package: WHM package name (used for WHM/cPanel)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    type = models.CharField(choices=PRODUCT_TYPES, max_length=35)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=False)
    whm_package = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class ProductAddOn(models.Model):
    """
    Purpose: ProductAddOn Model used to document
             related_name='addons' allows us to query;
             `product_object.addons` -> for all addons associated to Product
     @name: product addon name
     @description: product description
     @price: product addon price
     @available: is product addon available ?
     @product: product FK
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=False)
    product = models.ManyToManyField(Product, related_name='addons')

    def __str__(self):
        return self.name


class ProductConfiguration(models.Model):
    """
    Purpose: Every product has a different configuration (hostname, os, control panel, etc)
             This abstracts it using Option and OptionItem
     @name: product configuration name
     @description: product configuration description
     @product: product FK
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    product = models.ManyToManyField(Product, related_name='configs')

    def __str__(self):
        return self.name


class ProductConfigurationOption(models.Model):
    """
    Purpose: Product Configuration Option Model used to map certain options to configurations
    @name: option name
    @type: option form type
    @sort: sort order
    @available: is option available for configuration ?
    @configuration: product configuration FK
    """
    name = models.CharField(max_length=50)
    type = models.CharField(choices=FORM_TYPES, max_length=50)
    sort = models.PositiveIntegerField()
    available = models.BooleanField(default=False)
    configuration = models.ForeignKey(ProductConfiguration, related_name='options')

    class Meta:
        """
        Purpose: Meta class for initial QuerySet by Dango-Admin
        """
        ordering = ('sort', 'configuration')

    def __str__(self):
        return self.name


class ProductConfigurationOptionItem(models.Model):
    """
    Purpose: Product Configuration Option Item Model used to map items to options
    @name: option item name
    @price: option item price
    @sort: option item sort
    @option: product configuration option FK
    """
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sort = models.PositiveIntegerField()
    option = models.ForeignKey(ProductConfigurationOption, related_name='items')

    def __str__(self):
        return self.name
