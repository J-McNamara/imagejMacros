// http://imagej.nih.gov/ij/macros/DeconvolutionDemo.txt
//
// This macro demonstrates the use of frequency domain convolution
// and deconvolution. It opens a samples image, creates a point spread
// function (PSF), adds some noise (*), blurs the image by convolving it
// with the PSF, then de-blurs it by deconvolving it with the same PSF.
//
// * Why add noise? - Robert Dougherty
// Regarding adding noise to the PSF, deconvolution works by
// dividing by the PSF in the frequency domain.  A Gaussian
// function is very smooth, so its Fourier, (um, Hartley)
// components decrease rapildy as the frequency increases.  (A
// Gaussian is special in that its transform is also a
// Gaussian.)  The highest frequency components are nearly zero.
// When FD Math divides by these nearly-zero components, noise
// amplification occurs.  The noise added to the PSF has more
// or less uniform spectral content, so the high frequency
// components of the modified PSF are no longer near zero,
// unless it is an unlikely accident.

  if (!isOpen("bridge.gif")) run("Bridge (174K)");
  if (isOpen("PSF")) {selectImage("PSF"); close();}
  if (isOpen("Blurred")) {selectImage("Blurred"); close();}
  if (isOpen("Deblurred")) {selectImage("Deblurred"); close();}
  newImage("PSF", "8-bit black", 512, 512, 1);
  makeOval(246, 246, 20, 20);
  setColor(255);
  fill();
  run("Select None");
  run("Gaussian Blur...", "radius=8");
  run("Add Specified Noise...", "standard=2");
  run("FD Math...", "image1=bridge.gif operation=Convolve image2=PSF result=Blurred do");
  run("FD Math...", "image1=Blurred operation=Deconvolve image2=PSF result=Deblurred do");