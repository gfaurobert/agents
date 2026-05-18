#!/usr/bin/env bash
set -euo pipefail

agents_skills="${HOME}/.agents/skills"
hermes_skills_dir="${HOME}/.hermes/skills"
hermes_custom="${hermes_skills_dir}/custom"

if [[ ! -d "${agents_skills}" ]]; then
  echo "error: ${agents_skills} does not exist" >&2
  exit 1
fi

if [[ ! -d "${hermes_skills_dir}" ]]; then
  mkdir -p "${hermes_skills_dir}"
fi

if [[ -e "${hermes_custom}" && ! -L "${hermes_custom}" ]]; then
  echo "error: ${hermes_custom} exists and is not a symlink" >&2
  exit 1
fi

ln -sfn "${agents_skills}" "${hermes_custom}"
echo "linked ${hermes_custom} -> ${agents_skills}"
