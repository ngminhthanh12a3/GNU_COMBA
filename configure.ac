#-------------------------------------------------------------------------
# Project metadata
#-------------------------------------------------------------------------

m4_define( proj_name,         [LLM Project])
m4_define( proj_maintainer,   [Vu-Minh-Thanh Nguyen nvmthanh@hcmus.edu.vn])
m4_define( proj_abbreviation, [llm-p])

#-------------------------------------------------------------------------
# Project version information
#-------------------------------------------------------------------------
# Version information is meant to be managed through a version control
# system's tags and revision numbers. In a working copy the version will
# not be defined here (you should just use the version control system's
# mechanisms). When we make a distribution then we can set the version
# here as formed by the scripts/vcs-version.sh script so that the
# distribution knows what version it came from. If you are not using
# version control then it is fine to set this directly.

m4_define( proj_version, [0.0.0])

#-------------------------------------------------------------------------
# Setup
#-------------------------------------------------------------------------

AC_INIT(proj_name,proj_version,proj_maintainer,proj_abbreviation)
AC_CONFIG_SRCDIR([src/main.py])

#-------------------------------------------------------------------------
# --with-provider
#-------------------------------------------------------------------------

AC_ARG_WITH(provider,
  AS_HELP_STRING([--with-provider],[Provider to infer Large language model]),
  [provider="${with_provider}"],
  [provider=llamacpp])

AC_SUBST([provider])
AC_MSG_NOTICE([using provider: ${provider}])

#-------------------------------------------------------------------------
# --with-model
#-------------------------------------------------------------------------

AC_ARG_WITH(model,
  AS_HELP_STRING([--with-model],[Large language model to use]),
  [model="${with_model}"],
  [model="manual_Mistral_7B"])

AC_SUBST([model])
AC_MSG_NOTICE([using model: ${model}])

#-------------------------------------------------------------------------
# --with-max-token
#-------------------------------------------------------------------------

AC_ARG_WITH(max_token,
  AS_HELP_STRING([--with-max_token],[Max output tokens]),
  [max_token="${with_max_token}"],
  [max_token="2048"])

AC_SUBST([max_token])
AC_MSG_NOTICE([using max token: ${max_token}])

AC_ARG_WITH(temperature,
  AS_HELP_STRING([--with-temperature],[Temperature]),
  [temperature="${with_temperature}"],
  [temperature="0.85"])

AC_SUBST([temperature])
AC_MSG_NOTICE([using temperature: ${temperature}])

#-------------------------------------------------------------------------
# --with-samples
#-------------------------------------------------------------------------

AC_ARG_WITH(samples,
  AS_HELP_STRING([--with-samples],[Number of samples for each problem]),
  [samples="${with_samples}"],
  [samples="1"])

AC_SUBST([samples])
AC_MSG_NOTICE([using samples: ${samples}])


#-------------------------------------------------------------------------
# Output
#-------------------------------------------------------------------------

AC_CONFIG_FILES([Makefile])
AC_OUTPUT