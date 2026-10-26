/* CDE Toolkit settings for this deployment. Nothing here is secret: it is all public.
   clientId        the Client ID of your production APS app (sign-in uses PKCE, so there is no
                   client secret). Leave it empty to let each user paste their own Client ID.
   contactEndpoint where the Contact page sends messages, e.g. https://api.web3forms.com/submit
   contactAccessKey the form service's access key (Web3Forms access keys are safe to publish)
   contactEmail    optional address shown on the Contact page as an alternative (leave empty
                   to keep your email private)
   linkedinUrl     optional https:// link shown on the About page */
window.CDETK_CONFIG = {
  clientId: '',
  contactEndpoint: '',
  contactAccessKey: '',
  contactEmail: '',
  linkedinUrl: ''
};
