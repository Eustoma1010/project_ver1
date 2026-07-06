from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.products.models import Farm, Product, Category

User = get_user_model()

class FarmViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.farmer = User.objects.create_user(username='farmer', password='test123', role='FARMER')
        self.buyer = User.objects.create_user(username='buyer', password='test123', role='BUYER')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.farm = Farm.objects.create(name='Test Farm', region='North', owner=self.farmer, status='PENDING_ADMIN')

    def test_farm_registration_page_access(self):
        # Create a user without an associated farm
        new_user = User.objects.create_user(username='newfarmer', password='test123', role='FARMER')
        self.client.login(username='newfarmer', password='test123')
        response = self.client.get(reverse('farm:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'farm/register.html')

    def test_farm_pending_approval(self):
        self.client.login(username='farmer', password='test123')
        response = self.client.get(reverse('farm:home'))
        self.assertContains(response, 'Chờ duyệt')

    def test_dashboard_redirect_for_unapproved(self):
        self.client.login(username='farmer', password='test123')
        response = self.client.get(reverse('farm:dashboard'))
        self.assertRedirects(response, reverse('farm:home'))

    def test_dashboard_access_after_approval(self):
        self.farm.status = 'APPROVED'
        self.farm.save()
        self.client.login(username='farmer', password='test123')
        response = self.client.get(reverse('farm:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'farm/dashboard.html')

    def test_admin_reports_access(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/reports/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/reports.html')

    def test_products_list_access_after_approval(self):
        self.farm.status = 'APPROVED'
        self.farm.save()
        self.farmer.role = 'FARMER'
        self.farmer.save()
        self.client.login(username='farmer', password='test123')
        response = self.client.get(reverse('farm:products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'farm/products.html')

    def test_product_approval_flow(self):
        # Create Category and Product
        category = Category.objects.create(name='Rau củ', slug='rau-cu')
        product = Product.objects.create(
            name='Rau cải organic',
            slug='rau-cai-organic',
            price=20000,
            unit='kg',
            farm=self.farm,
            category=category,
            status='PENDING_ADMIN'
        )
        
        # Test Admin approval
        self.client.login(username='admin', password='admin123')
        # Check GET rendering with product
        response = self.client.get('/admin/reports/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rau cải organic')
        
        # POST Admin approve
        response = self.client.post('/admin/reports/', {
            'action': 'approve_product',
            'product_id': product.id
        })
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.status, 'PENDING_AUDITOR')
        
        # Test Auditor approval
        auditor = User.objects.create_user(username='auditor', password='auditor123', role='AUDITOR')
        self.client.login(username='auditor', password='auditor123')
        
        # Check GET rendering with product
        response = self.client.get(reverse('farm:auditor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rau cải organic')
        
        # POST Auditor approve
        response = self.client.post(reverse('farm:auditor_dashboard'), {
            'action': 'approve_product',
            'product_id': product.id
        })
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.status, 'APPROVED')
