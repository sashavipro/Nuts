"""home/tests.py."""

from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage


class HomeSetUpTests(WagtailPageTestCase):
    """Tests for basic page structure setup and HomePage creation."""

    def test_root_create(self):
        """Test that the root page gets created properly."""
        root_page = Page.objects.get(pk=1)
        assert root_page is not None

    def test_homepage_create(self):
        """Test that the HomePage can be successfully created and saved."""
        root_page = Page.objects.get(pk=1)
        homepage = HomePage(title="Home")
        root_page.add_child(instance=homepage)
        assert HomePage.objects.filter(title="Home").exists()


class HomeTests(WagtailPageTestCase):
    """Tests for homepage functionality and rendering."""

    def setUp(self):
        """Create a homepage instance for testing."""
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)

    def test_homepage_is_renderable(self):
        """Test if the homepage renders correctly without errors."""
        self.assertPageIsRenderable(self.homepage)

    def test_homepage_template_used(self):
        """Test if the homepage uses the correct HTML template."""
        response = self.client.get(self.homepage.url)
        self.assertTemplateUsed(response, "home/home_page.html")
