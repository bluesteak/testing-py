"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""
        # test that you see the RSVP form
        result = self.client.get("/")
        self.assertIn(b"<h2>Please RSVP</h2>", result.data)
        # test that you don’t see the party details
        self.assertNotIn(b"<h2>Party Details</h2>", result.data)


    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        # check that once we log in we see party details--but not the form!
        self.assertIn(b"<h2>Party Details</h2>", result.data)
        self.assertNotIn(b"<h2>Please RSVP</h2>", result.data)


    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        #a test that mel can't invite himself
        rsvp_info = {'name': "Mel Melitpolski", 'email': "mel@ubermelon.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        # check that once we log in we see party details--but not the form!
        self.assertNotIn(b"<h2>Party Details</h2>", result.data)
        self.assertIn(b"Sorry, Mel. This is kind of awkward.", result.data)


if __name__ == "__main__":
    unittest.main()
