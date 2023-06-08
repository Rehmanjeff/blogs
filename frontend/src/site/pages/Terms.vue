<template>
    <div class="min-h-screen ">
      <div class="container py-12 mx-auto">
        <div >
          <h1 class="mb-8 text-2xl font-bold">Terms of Service</h1>
  
          <div class="mb-8">
            <p class="text-sm text-gray-700 ">
              Welcome to our website and services! These Terms of Service ("Terms") govern your use of our platform. By
              accessing or using our website, you agree to be bound by these Terms and to comply with all applicable laws
              and regulations. If you do not agree with these Terms, you are prohibited from using our website.
            </p>
          </div>
  
        <div class="mb-8">
            <h2 class="mb-4 text-lg font-bold">User Conduct</h2>
            <p class="text-sm text-gray-700">
                When using our website, you agree to abide by the following rules of conduct:
            </p>
            <ul class="pl-6 mt-2 text-sm list-disc">
                <li class="text-gray-700">Do not violate any applicable laws or regulations.</li>
                <li class="text-gray-700">Respect the intellectual property rights of others.</li>
                <li class="text-gray-700">Refrain from engaging in any harmful or disruptive activities.</li>
                <li class="text-gray-700">Do not impersonate any person or entity.</li>
                <li class="text-gray-700">Avoid posting or transmitting any unauthorized or unsolicited promotional materials or spam.</li>
            </ul>
            </div>

            <!-- Section: Intellectual Property -->
            <div class="mb-8">
            <h2 class="mb-4 text-lg font-bold">Intellectual Property</h2>
            <p class="text-sm text-gray-700">
                All content and materials available on our website, including but not limited to text, graphics, logos, images,
                videos, and software, are the property of [Your Website Name] or its licensors and are protected by applicable
                intellectual property laws. You may not use, reproduce, distribute, or modify any of the content without prior
                written permission from us or the respective owner.
            </p>
            </div>

            <!-- Section: Limitation of Liability -->
            <div class="mb-8">
            <h2 class="mb-4 text-lg font-bold">Limitation of Liability</h2>
            <p class="text-sm text-gray-700">
                In no event shall [Your Website Name] or its affiliates, partners, or licensors be liable for any direct, indirect,
                incidental, special, or consequential damages arising out of or in any way connected with your use of our website,
                including but not limited to damages for loss of profits, data, or other intangible losses, even if we have been
                advised of the possibility of such damages.
            </p>
        </div>
  
          <div class="mb-8">
            <h2 class="mb-4 text-lg font-semibold">Privacy Policy</h2>
            <p class="text-sm text-gray-700 ">
              Please review our <RouterLink :to="{name:'Privacy'}" class="text-blue-500 underline">Privacy Policy</RouterLink> to understand
              how we collect, use, and protect your personal information.
            </p>
          </div>
  
          <div class="mt-8">
            <p class="text-sm text-gray-700 ">
              If you have any questions or concerns regarding these Terms, please contact us at
              <a href="mailto:rehman@timeahead.co" class="text-blue-500 underline">rehman@timeahead.co</a>.
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style>
.container {
  max-width: 800px;
}
</style>