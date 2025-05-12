import React, { useState, useEffect } from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { Disclosure } from '@headlessui/react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { ShieldCheckIcon } from '@heroicons/react/24/solid';

const navigation = [
  { name: 'Home', to: '/' },
  { name: 'How It Works', to: '/how-it-works' },
  { name: 'About', to: '/about' },
  { name: 'Contact', to: '/contact' },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

const Navbar = () => {
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 10;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };

    document.addEventListener('scroll', handleScroll);
    return () => {
      document.removeEventListener('scroll', handleScroll);
    };
  }, [scrolled]);

  return (
    <Disclosure as="nav" className={`fixed w-full z-10 ${scrolled ? 'bg-white shadow-md' : 'bg-transparent'} transition-all duration-300 ease-in-out`}>
      {({ open }) => (
        <>
          <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
            <div className="relative flex h-16 items-center justify-between">
              <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
                {/* Mobile menu button*/}
                <Disclosure.Button className="relative inline-flex items-center justify-center rounded-md p-2 text-gray-700 hover:bg-primary-500 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-600">
                  <span className="absolute -inset-0.5" />
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </Disclosure.Button>
              </div>
              <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                <div className="flex flex-shrink-0 items-center">
                  <ShieldCheckIcon className="h-8 w-auto text-primary-600" />
                  <span className="ml-2 text-xl font-bold text-primary-800">DeepFake Detection</span>
                </div>
                <div className="hidden sm:ml-6 sm:block">
                  <div className="flex space-x-4">
                    {navigation.map((item) => {
                      const isCurrent = location.pathname === item.to || 
                                        (location.pathname === '/' && item.to === '/');
                      return (
                        <RouterLink
                          key={item.name}
                          to={item.to}
                          className={classNames(
                            isCurrent
                              ? 'bg-primary-600 text-white'
                              : 'text-gray-700 hover:bg-primary-500 hover:text-white',
                            'rounded-md px-3 py-2 text-sm font-medium transition-all duration-200'
                          )}
                          aria-current={isCurrent ? 'page' : undefined}
                        >
                          {item.name}
                        </RouterLink>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <Disclosure.Panel className="sm:hidden">
            <div className="space-y-1 px-2 pb-3 pt-2">
              {navigation.map((item) => {
                const isCurrent = location.pathname === item.to || 
                                 (location.pathname === '/' && item.to === '/');
                return (
                  <Disclosure.Button
                    key={item.name}
                    as={RouterLink}
                    to={item.to}
                    className={classNames(
                      isCurrent
                        ? 'bg-primary-600 text-white'
                        : 'text-gray-700 hover:bg-primary-500 hover:text-white',
                      'block rounded-md px-3 py-2 text-base font-medium'
                    )}
                    aria-current={isCurrent ? 'page' : undefined}
                  >
                    {item.name}
                  </Disclosure.Button>
                );
              })}
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
};

export default Navbar; 