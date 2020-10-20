from django.test import TestCase
from model_mommy import mommy
from apps.api.models import *


# Create your model tests here.
class CountryTestCase(TestCase):
    def setUp(self):
        self.country = mommy.make(Country, _fill_optional=True)
        self.field_list = [
            field.name for field in Country._meta.get_fields()]

    def test_have_fields_needed_by_he_business(self):
        self.assertTrue('id' in self.field_list)
        self.assertTrue('name' in self.field_list)

    def tearDown(self):
        self.country.delete()


class ArtistTestCase(TestCase):
    def setUp(self):
        self.artist = mommy.make(Artist, _fill_optional=True)
        self.field_list = [
            field.name for field in Artist._meta.get_fields()]

    def test_have_fields_needed_by_he_business(self):
        self.assertTrue('id' in self.field_list)
        self.assertTrue('country' in self.field_list)
        self.assertTrue('name' in self.field_list)
        self.assertTrue('about' in self.field_list)

    def test_fk_have_country(self):
        self.assertTrue(self.artist.country.__class__ is Country)

    def tearDown(self):
        self.artist.delete()


class AlbumTestCase(TestCase):
    def setUp(self):
        self.album = mommy.make(Album, _fill_optional=True)
        self.field_list = [
            field.name for field in Album._meta.get_fields()]

    def test_have_fields_needed_by_he_business(self):
        self.assertTrue('id' in self.field_list)
        self.assertTrue('artist' in self.field_list)
        self.assertTrue('cover_page' in self.field_list)
        self.assertTrue('description' in self.field_list)
        self.assertTrue('release_year' in self.field_list)

    def test_fk_have_artist(self):
        self.assertTrue(self.album.artist.__class__ is Artist)

    def tearDown(self):
        self.album.delete()


class SongTestCase(TestCase):
    def setUp(self):
        self.song = mommy.make(Song, _fill_optional=True)
        self.field_list = [
            field.name for field in Song._meta.get_fields()]

    def test_have_fields_needed_by_he_business(self):
        self.assertTrue('id' in self.field_list)
        self.assertTrue('album' in self.field_list)
        self.assertTrue('name' in self.field_list)
        self.assertTrue('duration' in self.field_list)

    def test_fk_have_album(self):
        self.assertTrue(self.song.album.__class__ is Album)

    def tearDown(self):
        self.song.delete()
