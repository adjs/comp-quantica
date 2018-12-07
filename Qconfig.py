# Before you can use the jobs API, you need to set up an access token.
# Log in to the IBM Q experience. Under "Account", generate a personal
# access token. Replace 'PUT_YOUR_API_TOKEN_HERE' below with the quoted
# token string. Uncomment the APItoken variable, and you will be ready to go.

APItoken = '7c3c386c7ff83c2b1cf314f7b430e077d1e4a464de81db2b1f9a21c520a49744abda96846884e4b53c8ab54ae24f578cb19eadc1d994f63e177bd61d71bda875'
config = {
    'url': 'https://quantumexperience.ng.bluemix.net/api',

    # If you have access to IBM Q features, you also need to fill the "hub",
    # "group", and "project" details. Replace "None" on the lines below
    # with your details from Quantum Experience, quoting the strings, for
    # example: 'hub': 'my_hub'
    # You will also need to update the 'url' above, pointing it to your custom
    # URL for IBM Q.
    'hub': None,
    'group': None,
    'project': None
}

if 'APItoken' not in locals():
    raise Exception('a6e0c4d3ac6e7eb2c07b085440a891b1bfd356781f42389feba6903617ce30c2f2eae0ab47f30afff3992b3bfb34e905e5a565490d17d7b49374071c198078a6')
